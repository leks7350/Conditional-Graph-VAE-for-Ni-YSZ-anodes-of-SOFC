# Condition Graph VAE for Ni YSZ anodes of SOFC
В рамках данного проекта проводится анализ трехфазной стуктуры анодного слоя (Ni-YSZ) твердооксидного топливного элемента (ТОТЭ, SOFC).

Исходными данными для формирования датасета является данные работы "FIB-tomography data of Ni-YSZ anodes for Solid Oxide Fuel Cells (SOFC): Comparison of pristine and degraded materials (before/after redox cycling)" (Holzer, L., Pecho, O., Hocker, T., Iwanschitz, B., & Mai, A. (2020). FIB-tomography data of Ni-YSZ anodes for Solid Oxide Fuel Cells (SOFC): Comparison of pristine and degraded materials (before/after redox cycling) (Версия 1) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.4056538)

## Описание исходных данных: ##
Набор данных содержит трехмерные стеки изображений, полученные с помощью ионно-лучевой томографии (FIB-томографии) с анодов из никель-иттрий-сульфидного диоксида циркония (Ni-YSZ) для твердооксидных топливных элементов (SOFC).

Данные были собраны с трех различных анодов из Ni-YSZ (мелкозернистых, среднезернистых и крупнозернистых). Каждый из этих анодов исследовался сначала в исходном состоянии (после спекания и восстановления), а затем также в деградированном состоянии (после воздействия 8 окислительно-восстановительных циклов).

Затем 6 томограмм представлены в виде стопок 2D-изображений в формате TIFF в двух разных версиях: в виде изображений в оттенках серого (исходные данные) и в виде сегментированных изображений (Ni = белый, YSZ = серый и поры = черный).

### Срезы образцов ###
<table width=100%>
  <tr>
    <th>-</th>
    <th>Мелкозернистые (fine)</th>
    <th>Среднезернистые (medium)</th>
    <th>Крупнозернистые (coarse)</th>
  </tr>
  <tr>
    <td width="150">Исходное состояние (pristine)</td>
    <td><img width="200"  alt="pristine_fine" src="https://github.com/user-attachments/assets/d429f9fa-0a94-469e-b1a7-55eb1b2b399e" /></td>
    <td><img width="200" alt="pristine_medium" src="https://github.com/user-attachments/assets/91e15ab6-0b13-484f-877d-5fa88943f711" /></td>
    <td><img width="200"  alt="prisitne_coarse" src="https://github.com/user-attachments/assets/7f9cd6a0-4af8-4c64-9b61-38fc94208eb2" /></td>
  </tr>
  <tr>
    <td width="150">Деградация после 8 редокс-циклов (degraded)</td>
    <td><img width="200" alt="degraded_fine" src="https://github.com/user-attachments/assets/64e22a2b-da6f-4f60-a6e7-9cbc1a86d237" /></td>
    <td><img width="200"  alt="degraded_medium" src="https://github.com/user-attachments/assets/96444005-f968-41a9-86d6-74350fc24864" /></td>
    <td><img width="200"  alt="degraded_coarse" src="https://github.com/user-attachments/assets/6a2e0cbe-2488-4a19-90bb-8a96ee1b298c" /></td>
  </tr>
</table>

### Общий вид стека изображений ###
<img width="400"  alt="6Segment_01" src="https://github.com/user-attachments/assets/21bc7c09-c1ff-4404-90ed-e4339c4405e0" />

Размеры стеков:
<ul>
  <li><b>pristine_fine</b>    (995x1304x733 вокселей),  </li>
  <li><b>pristine_medium</b>  (960x1110x610 вокселей)</li>
  <li><b>pristine_coarse</b>  (744x1417x456 вокселей)</li>
  <li><b>degraded_fine</b>    (1171x1343x461 вокселей)</li>
  <li><b>degraded_medium</b>  (1318x1520x459 вокселей)</li>
  <li><b>degraded_coarse</b>  (1368x1630x500 вокселей)</li> 
</ul>










