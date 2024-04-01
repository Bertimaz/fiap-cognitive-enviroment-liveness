from tools.functions import count_faces,recognize_user


with open(f'C:\\Users\\alber\\Documents\\Projetos - Dados\\cognitive-enviromment-integrado\\imgs\\selfie_oscar.jpg', "rb") as file:
  img_file = file.read()
  bytes_file_target = bytearray(img_file)
n=count_faces(bytes_file_target)
print(n)



with open(f'imgs\\nic4.png', "rb") as file:
  img_file = file.read()
  bytes_file_target = bytearray(img_file)

print(recognize_user(bytes_file_target))