from PIL import Image, ImageDraw, ImageFont, ImageOps

def generate_quotes_image (image_path, quote):
    height = 614
    width = 614

    base_img = Image.open(image_path).convert('RGBA')
    base_img = ImageOps.fit(base_img, (width, height), Image.ANTIALIAS, 0, (0.5, 0.5))

    img = Image.new('RGBA', (height, width), color=(0,0,0,150))

    # Quote
    sentence = quote

    font = ImageFont.truetype('./fonts/Raleway-Medium.ttf', 30)

    draw = ImageDraw.Draw(img)

    sum = 0
    for letter in sentence:
        sum += draw.textsize(letter, font=font)[0]

    average_length_of_letter = sum/len(sentence)
    #find the number of letters to be put on each line
    number_of_letters_for_each_line = (height/1.618)/average_length_of_letter
    incrementer = 0
    fresh_sentence = ''
    #add some line breaks
    for letter in sentence:
        if(letter == '-'):
            fresh_sentence += '\n\n' + letter
        elif(incrementer < number_of_letters_for_each_line):
            fresh_sentence += letter
        else:
            if(letter == ' '):
                fresh_sentence += '\n'
                incrementer = 0
            else:
                fresh_sentence += letter
        incrementer+=1
    print(fresh_sentence)

    dim = draw.textsize(fresh_sentence, font=font)

    new_height = dim[0]
    new_width = dim[1]

    x_origin = (height/2 - new_height/2)
    y_origin = (width/2 - new_width/2)

    draw.text((x_origin,y_origin), fresh_sentence, align="center", font=font, fill=(200,200,200))

    # Save the image
    out = Image.alpha_composite(base_img, img)
    file_path = './processed_images/'+image_path.split('/')[-1].split('.')[0] + '.jpg'
    image_jpg = out.convert('RGB')
    image_jpg.save(file_path)
    return file_path