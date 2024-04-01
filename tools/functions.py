# from connection import connect_aws
from tools.connection import connect_aws
from PIL import Image
import cv2
import numpy as np
import tensorflow as tf

def recognize_user(image): 
  """
  Retorna nome do usuário de uma imagem
  Variavel
  image: imagem em bytes
  retorna str
  """
  #Conecta com AWS
  session=connect_aws()
  #aBRINDO CLINETE
  client=session.client('rekognition',region_name='us-east-2')
  #Obtendo dados da imagem
  response=client.search_faces_by_image(
     Image={'Bytes': image
     },
    CollectionId='user-faces'
  )
  try:
    #Obtendo face_id com maior similaridade
    face_id_max_similarity=response['FaceMatches'][0]['Face']['FaceId']
  except IndexError:
    return 'Usuário não identificado'
  #Obtendo User de com maior similaridade
  response=client.search_users(
    FaceId=face_id_max_similarity,
    CollectionId='user-faces'
  )
  #Retorna nome do usuário
  return response['UserMatches'][0]['User']['UserId']

def count_faces(img):
  """
  Função que conta numero de pessoas
  variavel
  img - Imagem em bytes
  retorna número de imagens
  """
  #Conecta com AWS
  session=connect_aws()
  #aBRINDO CLINETE
  client=session.client('rekognition',region_name='us-east-2')
  #Criando requisição
  response=client.detect_faces(
      Image={'Bytes':img}
      # Attributes=['All']
  )
  #Contando numero de pessoas
  n= len(response['FaceDetails'])
  return n



def is_valid_photo(bytes_file):
  """
  Fonte: https://pyimagesearch.com/2019/03/11/liveness-detection-with-opencv/
  Function that returns
  True if the picture is valid(A.K.A a real picture)
  False if the picture in invalid(picture of a picture,phone etc..)

  Variables:
   img: photo in the bytes format
  """
  BS=8
  #iniciliaza lista
  data=[]
  #Inicializa modelo
  model=tf.keras.models.load_model('modelos/fraud_detector_v01.keras')
  #Le arquivo com cv2
  nparr = np.frombuffer(bytes_file, np.uint8)
  img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
  #Resize
  img=cv2.resize(img,(32,32))
  #Adiciona a lista
  data.append(img)
  #Prepara lista
  data= np.array(data, dtype="float") / 255.0
  #Faz a previsão
  predictions = model.predict(x=data, batch_size=BS)

  for prediction in predictions:
      if prediction.argmax(axis=0)==1:
          return True
      else:
          return False

def get_bounding_box(img_path:str):
  """
  Get Bounding box for first face in image
  Variable: path= path to the imagem file
  Returns  top,left,width,height
  """
  #Get image as bytes
  with open(img_path, "rb") as file:
      img_file = file.read()
      bytes_file_target = bytearray(img_file)
  #Conecta com AWS
  session=connect_aws()
  #aBRINDO CLINETE
  client=session.client('rekognition',region_name='us-east-2')
  #Criando requisição
  response=client.detect_faces(
      Image={'Bytes':bytes_file_target},
      Attributes=['ALL']
  )
  # Pega informações da bounding box
  width=response['FaceDetails'][0]['BoundingBox']['Width']
  height=response['FaceDetails'][0]['BoundingBox']['Height']
  left=response['FaceDetails'][0]['BoundingBox']['Left']
  top=response['FaceDetails'][0]['BoundingBox']['Top']

  return top,left,width,height

def crop_image(img:Image, top:float,left:float,width:float,height:float):
  """
  crops Image
  Variabable: Image
  top,left,width,height
  Returns Cropped Image
  """
  # Calculate coordinates for cropping
  right = left + width
  bottom = top + height
  # Crop the image
  cropped_image = img.crop((left*img.size[0], top*img.size[1], right*img.size[0], bottom*img.size[1]))
  #return the image
  return cropped_image 