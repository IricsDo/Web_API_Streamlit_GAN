import os
import base64
import time
import streamlit as st
from PIL import Image
from steganogan.models import SteganoGAN

@st.cache(allow_output_mutation=True)

def downloader(bin_file, file_label='File'):

    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

def get_base64_of_bin_file(bin_file):

    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):

    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return True
def set_gif_in_web(path, option):

    
    if option == "url": # example https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif

        st.markdown(f"![Alt Text]({path})")

    if option == "local": # example /home/rzwitch/Desktop/giphy.gif

        file_ = open(f"{path}", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',unsafe_allow_html=True)

if __name__ == '__main__':

    # Init
    steganogan = SteganoGAN.load(path = "models/demo_div2k_with_deep-data_1_basic.steg", cuda=False, verbose=True)
    st.set_page_config(page_title="My App", page_icon="🇻🇳", layout='wide', initial_sidebar_state='auto')

    _ ,_ ,_, pos4, _, _, pos7 = st.beta_columns([1, 1, 1, 3, 1, 1, 0.75])
    with pos4:
        st.title("MY EXAMPLE WEBSITE !!")
    
    with pos7:
        date = st.date_input(label="To Day Is", help= "Ho Chi Minh City, UTC+7")

    pos8, _, _, _, pos12 = st.beta_columns([3, 1, 1, 1, 3])
    with pos8:
        st.header("Upload Image You Want To Hidden Text")

    pos13, _, _, _, pos17, = st.beta_columns([2, 1, 0.5, 0.5, 2])
    with pos13:
        st.set_option('deprecation.showfileUploaderEncoding', False)
        imgData = st.file_uploader("", type=['png', 'jpg', 'jpeg'], key=0)

    pos18, _, _, _, pos22, = st.beta_columns([2, 1, 0.5, 0.5, 2])
    with pos18:
        message_in = st.text_input(label="Enter Your Message Here", value="", max_chars=None, key=None, type="default", help=None)
    
    mode = st.radio(label="What's the image quality you want to choose?", options=("Bad", "Good", "Very Good"))
    pos23, pos24 = st.beta_columns([1, 0.5])
    with pos23:
        if st.button("Encoder"):

            if imgData is not None and message_in is not None:

                set_png_as_page_bg('background/pexels-photo-733852.png')
                # st.write("Number Image Upload To Day in Website: {}".format(imgData.id))
                imageProces = Image.open(imgData)
                pos1 = st.beta_container()

                with pos1:
                    st.header("Your Image")
                    st.image(imageProces, caption=None, width=600, use_column_width=None, \
                                        clamp=False, channels='RGB', output_format='auto')
                time.ctime()

                # if os.path.isfile(os.path.join("user_Image_upload", imgData.name)):
                #     print("File already exists!")

                # else:
                name = time.ctime().replace(" ", "$") + imgData.name
                imageProces.save(os.path.join("user_Image_upload", name))

                # if os.path.isfile(os.path.join("cache", imgData.name)):
                #     print("File already exists!")
                # else:
                with st.spinner('Encode ....'):
                    steganogan.encode(os.path.join("user_Image_upload", name), os.path.join("cache", name) , message_in)
                pos2 = st.beta_container()
                with pos2:
                    st.header("Your Result")
                    st.image(os.path.join("cache", name), caption=None, width=600, use_column_width=None, \
                                        clamp=False, channels='RGB', output_format='auto')

                st.markdown(downloader(os.path.join("cache", name), 'Picture'), unsafe_allow_html=True)
                
            else:
                st.error("MUST HAVE IMAGE OR MESSAGE FOR ENCODER !!!")
        else:
            set_png_as_page_bg('background/pexels-karolina-grabowska-4397899.png')

    with pos12:
        st.header("Upload Image You Want To Find Text")

    with pos17:
        st.set_option('deprecation.showfileUploaderEncoding', False)
        imgData_ = st.file_uploader("", type=['png', 'jpg', 'jpeg'], key=1)

    with pos22:
        if st.button("Decoder"):

            if imgData_ is not None:

                # st.header("Your Image")
                st.image(os.path.join("cache", imgData_.name), caption=None, width=None, use_column_width=None, \
                                        clamp=False, channels='RGB', output_format='auto')
                with st.spinner('Decode ....'):
                    message_out = steganogan.decode(os.path.join("cache", imgData_.name))

                st.write("Your message in here -->: " + message_out)
            else:
                pass
        else:
            pass

