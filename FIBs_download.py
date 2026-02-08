#!pip install imagecodecs -q

import os
import zipfile
import numpy as np
import urllib.request
import tifffile as tiff
import imagecodecs

def zip_files(file_list, zip_path, file_extention=''):
    # Создаём объект ZipFile
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Проходимся по всем файлам из списка (словаря)
        for name in file_list:
          fname = f"{name}{file_extention}"
          # Добавляем файл в архив
          zipf.write(fname, fname)

def zip_directory(directory_path, zip_path):
    # Создаём объект ZipFile
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Проходимся по всем файлам и поддиректориям
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Определяем путь внутри архива относительно исходной директории
                arcname = os.path.relpath(file_path, os.path.dirname(directory_path))
                # Добавляем файл в архив
                zipf.write(file_path, arcname)

def download(dir, url_dict, name_dict):
  for name, url in url_dict.items():
    fname = f"{name}.zip"
    print(f'download: {fname}')
    urllib.request.urlretrieve(url, fname)
    with zipfile.ZipFile(fname, 'r') as zip_ref:
      print(f'unzip: {fname}')
      zip_ref.extractall(dir)
      os.rename(os.path.join(dir,name) , os.path.join(dir, name_dict.get(name)))
  print(f'Загрузка завершена')

  print('Архивируем')
  zip_files(url_dict, os.path.join('./4056538_archive_segmented.zip'), '.zip')

  return dir

def load_tiff_stack(folder_path):
  tiff_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.tif')])
  stack = np.stack([tiff.imread(os.path.join(folder_path, f)) for f in tiff_files])
  return stack.astype(np.uint8)

def stack_FIBs(input_seg_directory):
  all_items = os.listdir(input_seg_directory)
  folders = [item for item in all_items if os.path.isdir(os.path.join(input_seg_directory, item))]

  stacks = []

  for dir in folders:
    # Переводим .tiff в 3D-массив
    stack = load_tiff_stack(os.path.join(input_seg_directory,dir))
    tom = np.zeros_like(stack, dtype=np.uint8)
    tom[stack == 0] = 0    # pore
    tom[stack == 100] = 1  # YSZ
    tom[stack == 200] = 2  # Ni
    tom[stack == 255] = 2  # Ni
    tom[stack == 1] = 0
    tom[stack == 2] = 1
    tom[stack == 3] = 2
    tom[stack == 36] = 0
    tom[stack == 76] = 1
    tom[stack == 121] = 1
    tom[stack == 194] = 2
    tom[stack == 150] = 2

    stacks.append([f'{dir}', tom])
    print(f'"{dir}" shape: {tom.shape}')

  return stacks

def extract_patches_with_overlap(voxel_array, cube_size=456, overlap_fraction=0.5):
    '''
    Извлекает кубические патчи с заданным процентом перекрытия

    Аргументы:
        voxel_array: 3D массив вокселей
        cube_size: размер кубического патча
        overlap_fraction: доля перекрытия между соседними патчами (0-1)
    '''
    if overlap_fraction < 0:
      overlap_fraction = 0
    elif overlap_fraction > 1:
        overlap_fraction = 1

    overlap = int(cube_size * overlap_fraction)
    stride = cube_size - overlap

    shape = voxel_array.shape

    # Проверяем, что cube_size не превышает размеры массива
    if cube_size > shape[0] or cube_size > shape[1] or cube_size > shape[2]:
        raise ValueError(f"cube_size={cube_size} превышает размеры массива {shape}")

    # Рассчитываем количество патчей по каждой оси
    n_z = max(1, (shape[0] - overlap) // stride)
    n_y = max(1, (shape[1] - overlap) // stride)
    n_x = max(1, (shape[2] - overlap) // stride)

    patches = []

    # Извлекаем патчи
    for i in range(n_z):
        for j in range(n_y):
            for k in range(n_x):
                z_start = min(i * stride, shape[0] - cube_size)
                y_start = min(j * stride, shape[1] - cube_size)
                x_start = min(k * stride, shape[2] - cube_size)

                patch = voxel_array[
                    z_start:z_start+cube_size,
                    y_start:y_start+cube_size,
                    x_start:x_start+cube_size
                ]
                patches.append(patch)

    return np.array(patches)

def save_cubes(cubes, filename):
  # Сохраняем в NPY
  np.save(filename, cubes)
  # print(f"Воксели сохранены в {filename}")

def stack_to_3D(stacks, cube_size, overlap_fraction, output_dir):
  filelist = []
  for stack in stacks:
    #Разбиваем
    patches  = extract_patches_with_overlap(stack[1], cube_size=cube_size, overlap_fraction=overlap_fraction)
    print(f'{stack[0]}: {len(patches)} патчей')

    #Сохраняем
    for i in range(len(patches)):
      cube = patches[i]  # cube.shape = (448, 448, 448)
      filename= os.path.join(output_dir,f'3D_{stack[0]}_{i}.npy')
      save_cubes(cubes=cube, filename= filename)
      filelist.append(filename)
    print(f'{stack[0]}: сохранено {len(patches)} файлов NPY')

  return filelist

def stack_to_2D(stacks, cube_size, overlap_fraction, output_dir):
  filelist = []
  for stack in stacks:
    #Разбиваем
    patches  = extract_patches_with_overlap(stack[1], cube_size=cube_size, overlap_fraction=overlap_fraction)
    print(f'{stack[0]}: {len(patches)} патчей')
    counter = 0

      #Сохраняем
    for i in range(len(patches)):
      cube = patches[i]
      for n in range(cube.shape[0]):
        img = cube[n, :, :]
        filename = os.path.join(output_dir,f'2D_{stack[0]}_{i}{n}.npy')
        save_cubes(cubes=img, filename= filename)
        filelist.append(filename)
        counter +=1

    print(f'{stack[0]}: сохранено {counter} файлов NPY')

  return filelist

def get_data(output='2D', output_dir='./data/', cube_size=456, overlap_fraction=0.5, balance=False, to_archive=False):
  '''
  Функция загрузки FIB снимков и перевода их в требуемую размерность
  ------------------------------------------------------------------
  Аргументы:
    output: string
      Требуемая размерность выходных данных
      Значения:
        2D - двумерный выход .shape(y,x)
        3D - трехмерный выход .shape(z,y,x)
    output_dir: string
      Директория для сохранения обработанных данных

    cube_size: integer
      размер кубического патча

    overlap_fraction: float (0-1)
      доля перекрытия между соседними патчами (0-1)

    balance: boolean
      Требуется ли балансировать выходные классы по количеству (True, False)

    to_archive: boolean
      Требуется ли сохранить в архив выходные файлы
  '''

  input_seg_directory = './Segmented/'


  print('Загрузка датасета 4056538 из Zenodo.org')
  print(f'='*60)
  os.makedirs(input_seg_directory, exist_ok=True)
  os.makedirs(output_dir, exist_ok=True)

  segmented_urls = {
                '3_Rx36_Segmented': 'https://zenodo.org/records/4056538/files/3_Rx36_Segmented.zip',
                '4_Rx37_Segmented': 'https://zenodo.org/records/4056538/files/4_Rx37_Segmented.zip',
                '5_Rx38_Segmented': 'https://zenodo.org/records/4056538/files/5_Rx38_Segmented.zip',
                '6_Rx41-1_Segmented': 'https://zenodo.org/records/4056538/files/6_Rx41-1_Segmented.zip',
                '7_Rx41-2_Segmented': 'https://zenodo.org/records/4056538/files/7_Rx41-2_Segmented.zip',
                '8_Rx41-3_Segmented': 'https://zenodo.org/records/4056538/files/8_Rx41-3_Segmented.zip'
                }
  coarness_degradation_dict = {
                '3_Rx36_Segmented' : 'pristine_fine',
                '4_Rx37_Segmented' : 'pristine_medium',
                '5_Rx38_Segmented' : 'pristine_coarse',
                '6_Rx41-1_Segmented' : 'degraded_fine',
                '7_Rx41-2_Segmented' : 'degraded_medium',
                '8_Rx41-3_Segmented' : 'degraded_coarse'}

  segments = os.listdir(input_seg_directory)
  if len(segments) == 0:
    print('Загрузка сегментированных FIB снимков')
    dir = download(input_seg_directory, segmented_urls, coarness_degradation_dict)
    print(f'='*60)
  else:
    print('Cегментированных FIB снимки загружены ранее')
    dir = input_seg_directory

  print('Формирование снимков в stacks')
  stacks = stack_FIBs(dir)
  print(f'='*60)

  NPY_files = []

  print(f'Разделение объемных стаков на {output} патчи и сохранение NPY')
  if output == '3D':
    NPY_files = stack_to_3D(stacks, cube_size, overlap_fraction, output_dir)
  else:
    NPY_files = stack_to_2D(stacks, cube_size, overlap_fraction, output_dir)

  #Балансировка классов
  if balance:
    ''


  #Архивируем если требуется
  if to_archive:
    print(f'='*60)
    print(f'Архивируем файлы из папки {output_dir}')
    zip_files(NPY_files, f'./output_archive.zip')

  print(f'='*60)
  print(f'Выход: список {len(NPY_files)} файлов .npy ')

  return NPY_files

#npylist = get_data(output='2D', to_archive=True)
