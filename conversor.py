import os
import zipfile
import patoolib
from PIL import Image
import shutil

def move_images(output_folder):
    extracted_files = os.listdir(output_folder)
    
    for file in extracted_files:
        if os.path.isdir(os.path.join(output_folder, file)):
            for file_name in os.listdir(output_folder+'/'+file):
                shutil.move(output_folder+'/'+file+'/'+file_name, output_folder+'/'+file_name)
            shutil.rmtree(output_folder+'/'+file)
            print(f"Arquivos movidos de: {output_folder+'/'+file}, para: {output_folder}.")

def compress_images(output_folder):
    image_files = [f for f in os.listdir(output_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))] 
    for image_file in image_files:
        image_path = os.path.join(output_folder, image_file)
        image = Image.open(image_path)
        file_name, file_extension = os.path.splitext(image_path)
        image.save(file_name + '.jpg', quality=30)
    print("Imagens comprimidas.")

def rename_images(output_folder):
    files = os.listdir(output_folder)
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    images_length = len(image_files)

    for file in reversed(image_files):
        if os.path.isfile(os.path.join(output_folder, file)):
            new_name = f'{images_length}.jpg'
            os.rename(os.path.join(output_folder, file), os.path.join(output_folder, new_name))
            images_length -= 1
    print("Imagens renomeadas em ordem numérica.")

for file in os.listdir('fila'):
    output_folder = file[:-4]

    if file.endswith(('.cbz')):    
        zipfile.ZipFile('fila/' + file, 'r').extractall(output_folder)
        print(f"Arquivos cbz extraídos em {output_folder}.")

        move_images(output_folder)
        compress_images(output_folder)
        rename_images(output_folder)
    else: 
        patoolib.extract_archive('fila/' + file, outdir=output_folder, verbosity=-1)
        print(f"Arquivos cbr extraídos em {output_folder}.")

        move_images(output_folder)
        compress_images(output_folder)
        rename_images(output_folder)