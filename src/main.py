import os, shutil, re, sys
from textnode import TextNode, TextType
from textsplit import *

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    
    copy_path = './static'
    destination_path = './docs'
    delete_everything_inside_folder(destination_path)
    copy_everything_from_to(copy_path, destination_path)
    generate_pages_recursive('./content/', './template.html', destination_path, basepath)



    




def delete_everything_inside_folder(inside_folder):
    # First check if the folder actually exists
    if not os.path.exists(inside_folder):
        print(f"🚨 Oops, '{inside_folder}' doesn't exist!")
        return
    
    # Go through all items inside the folder
    for item in os.listdir(inside_folder):
        item_path = os.path.join(inside_folder, item)

        if os.path.isfile(item_path) or os.path.islink(item_path):
            # Remove file or symbolic link
            os.remove(item_path)
            print(f"🗑️ File/link deleted: {item_path}")

        elif os.path.isdir(item_path):
            # Remove directories (with their contents)
            shutil.rmtree(item_path)
            print(f"🗑️ Directory and its contents deleted: {item_path}")


def copy_everything_from_to(from_path, to_path):
    if not os.path.exists(from_path):
        print(f"🚨 Oops, '{from_path}' path, which you wanna copy FROM, doesn't exist!")
        return
    
    if not os.path.exists(to_path):
        os.mkdir(to_path)
        print(f"📁 Destination folder '{to_path}' created.")

    for item in os.listdir(from_path):
        new_from_path = os.path.join(from_path, item)
        new_to_path = os.path.join(to_path, item)

        if os.path.isfile(new_from_path):
            # If it's a file, simply copy it!
            shutil.copy(new_from_path, new_to_path)
            print(f"📄 Copied file: '{new_from_path}' → '{new_to_path}'")

        elif os.path.isdir(new_from_path):
            # If it's a directory, use recursion to copy its contents
            print(f"📂 Found directory: '{new_from_path}'. Going deeper...")
            copy_everything_from_to(new_from_path, new_to_path)


def extract_title(markdown):
    match = re.match(r'^#\s+(.*)', markdown.strip())

    if match:
        return match.group(1).strip()
    else:
        raise ValueError("🚨 No H1 title found in markdown!")
    
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    
    with open(from_path, 'r', encoding='utf-8') as file:
        source_content = file.read()
    
    with open(template_path, 'r', encoding='utf-8') as file:
        template_content = file.read()
 
    html_content = markdown_to_html_node(source_content)

    text_title = extract_title(source_content)

    final_result = template_content.replace('{{ Title }}', text_title).replace('{{ Content }}', html_content.to_html())

    final_result = final_result.replace('href="/', f'href="{basepath}')
    final_result = final_result.replace('src="/', f'src="{basepath}')


    with open(dest_path, 'w', encoding='utf-8') as file:
        file.write(final_result)

    print("✨ Template filled successfully!")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dir_path_content):
        print(f"🚨 Oops, '{dir_path_content}' path, which you wanna generate FROM, doesn't exist!")
        return
    
    os.makedirs(dest_dir_path, exist_ok=True)
    print(f"📁 Ensured destination folder '{dest_dir_path}' exists.")

    for item in os.listdir(dir_path_content):
        new_from_path = os.path.join(dir_path_content, item)
        new_to_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(new_from_path):
            # If it's a file, simply copy it!
            if item.endswith('.md'):
                html_filename = os.path.splitext(item)[0] + ".html"
                dest_file_path = os.path.join(dest_dir_path, html_filename)
                generate_page(new_from_path, template_path, dest_file_path, basepath)

        elif os.path.isdir(new_from_path):
            # If it's a directory, use recursion to copy its contents
            print(f"📂 Found directory: '{new_from_path}'. Going deeper...")
            generate_pages_recursive(new_from_path, template_path, new_to_path, basepath)





    
    


main()