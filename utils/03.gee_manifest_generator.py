!mkdir json
import glob
import json
import os
from datetime import datetime

# setup paths and environment
output_path = '/content/json/'
cloud_path = 'gs://gee-ingest-fao/GRACE'
gee_asset_path = 'projects/gee-ait/assets/GRACE/MASS_GRIDS/LAND'
manifest_dir = output_path

# list all the image data, the manifest will be based on image properties
lst = os.listdir('/content/GRACE/')

#----------------------------------------------------------------------

# manifest generator
for i, image in enumerate(lst):
  tileset_id = str(time_time_bounds['time_beginning_YMD'][i])+'_'+str(time_time_bounds['time_end_YMD'][i])
  manifest_name = '{}/{}'.format(gee_asset_path, tileset_id)

  manifest_tilesets = []
  manifest_bands = []
  # print(manifest_name)

  _tileset = {
      'id': tileset_id,
      'sources': [
          {
              'uris': [
                  '{}/{}'.format(cloud_path, image)
              ]
          }
      ]
  }

  _band = {
    'id': "lwe_thickness_csr",
    'tileset_id': tileset_id
  }

  manifest_tilesets.append(_tileset)
  manifest_bands.append(_band)

  ## properties
  manifest_properties = {}
  manifest_properties['CSR_START_TIME'] = int(time_time_bounds['time_beginning_ms'][i])
  manifest_properties['CSR_end_TIME'] = int(time_time_bounds['time_end_ms'][i])
  # start_index = 3
  # for _property in properties:
  #     manifest_properties[_property] = image[start_index]
  #     start_index += 1

  # start time
  manifest_start_time = {
      'seconds': int(time_time_bounds['time_beginning_ms'][i]/1000)
  }

  # end time
  manifest_end_time = {
      'seconds': int(time_time_bounds['time_end_ms'][i]/1000)
  }

  final_manifest = {
    'name': manifest_name,
    'tilesets': manifest_tilesets,
    'bands': manifest_bands,
    'start_time': manifest_start_time,
    'end_time': manifest_end_time,
    'properties': manifest_properties
  }
  # print(final_manifest)
  with open('{}{}.json'.format(manifest_dir, tileset_id), 'w') as manifest_file:
    json_string = json.dumps(final_manifest, ensure_ascii=False, indent=4)
    manifest_file.write(json_string)

!zip -r jsonGrace.zip /content/json/*.json >> /dev/null