import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import Canvas, Frame, Scrollbar, Text, Toplevel
from PIL import Image, ImageTk, ImageDraw, ImageSequence, ImageFont, ImageGrab
import cv2
import numpy as np
import threading
import os
from pathlib import Path
import json
from datetime import datetime
import re
import subprocess
import platform
import tempfile
import sys # <<< NEW >>>
import collections
import requests
import base64
import io
import shutil
import time
from io import BytesIO
import webbrowser
from functools import partial

# ===== MOCKUP PROMPTS =====
# Mockup Print Type - Front
MOCKUP_PROMPTS_PRINT_FRONT = {
    "T-shirt": "Vẽ lại thiết kế trên mặt trước mockup áo T-shirt, phong cách tự nhiên, ánh sáng thật, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024.",
    "Hooded": "Vẽ lại thiết kế trên mặt trước mockup áo Hoodie, phong cách tự nhiên, ánh sáng thật, bối cảnh lifestyle, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024.",
    "Sweatshirt": "Vẽ lại thiết kế trên mặt trước mockup áo Sweatshirt, phong cách tự nhiên, ánh sáng mềm, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024.",
    "Baby Rib Bodysuit": "Vẽ lại thiết kế trên mặt trước mockup áo Baby Rib Bodysuit, phong cách tự nhiên, ánh sáng mềm, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024.",
    "Hat": "Vẽ lại thiết kế trên mặt trước mockup mũ/nón, phong cách tự nhiên, ánh sáng thật, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024.",
    "Mug": "Vẽ lại thiết kế trên mockup cốc/ly, phong cách tự nhiên, ánh sáng thật, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024."
}

# Mockup Print Type - Back
MOCKUP_PROMPTS_PRINT_BACK = {
    "T-shirt": "Vẽ lại thiết kế trên mặt sau mockup áo T-shirt, góc nhìn từ phía sau, phong cách tự nhiên, ánh sáng thật, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024.",
    "Hooded": "Vẽ lại thiết kế trên mặt sau mockup áo Hoodie, góc nhìn từ phía sau, phong cách tự nhiên, ánh sáng thật, bối cảnh lifestyle, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024.",
    "Sweatshirt": "Vẽ lại thiết kế trên mặt sau mockup áo Sweatshirt, góc nhìn từ phía sau, phong cách tự nhiên, ánh sáng mềm, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024.",
    "Baby Rib Bodysuit": "Vẽ lại thiết kế trên mặt sau mockup áo Baby Rib Bodysuit, góc nhìn từ phía sau, phong cách tự nhiên, ánh sáng mềm, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024.",
    "Hat": "Vẽ lại thiết kế trên mặt sau mockup mũ/nón, góc nhìn từ phía sau, phong cách tự nhiên, ánh sáng thật, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024.",
    "Mug": "Vẽ lại thiết kế trên mockup cốc/ly, phong cách tự nhiên, ánh sáng thật, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024."
}

# Backward compatibility
MOCKUP_PROMPTS_PRINT = MOCKUP_PROMPTS_PRINT_FRONT

# Mockup Embroidery Type - Front
MOCKUP_PROMPTS_EMBROIDERY_FRONT = {
    "T-shirt": "Vẽ lại thiết kế trên mặt trước mockup áo T-shirt dạng thêu, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng tự nhiên, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024.",
    "Hooded": "Vẽ lại thiết kế trên mặt trước mockup áo Hoodie dạng thêu, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng tự nhiên, bối cảnh lifestyle, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024.",
    "Sweatshirt": "Vẽ lại thiết kế trên mặt trước mockup áo Sweatshirt dạng thêu, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng mềm, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024.",
    "Baby Rib Bodysuit": "Vẽ lại thiết kế trên mặt trước mockup Baby Rib Bodysuit dạng thêu, đường chỉ ngang rõ nét, phong cách thêu thật, dễ thương, có vật trang trí như gấu bông, chăn nhỏ. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024.",
    "Hat": "Vẽ lại thiết kế trên mặt trước mockup mũ dạng thêu, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng tự nhiên, bối cảnh lifestyle, có vật trang trí nhỏ. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024.",
    "Mug": "Vẽ lại thiết kế trên mockup ly sứ, phong cách tự nhiên, ánh sáng thật, bối cảnh đẹp, có vật trang trí như sách, cây, bàn gỗ. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024."
}

# Mockup Embroidery Type - Back
MOCKUP_PROMPTS_EMBROIDERY_BACK = {
    "T-shirt": "Vẽ lại thiết kế trên mặt sau mockup áo T-shirt dạng thêu, góc nhìn từ phía sau, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng tự nhiên, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024.",
    "Hooded": "Vẽ lại thiết kế trên mặt sau mockup áo Hoodie dạng thêu, góc nhìn từ phía sau, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng tự nhiên, bối cảnh lifestyle, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024.",
    "Sweatshirt": "Vẽ lại thiết kế trên mặt sau mockup áo Sweatshirt dạng thêu, góc nhìn từ phía sau, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng mềm, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024.",
    "Baby Rib Bodysuit": "Vẽ lại thiết kế trên mặt sau mockup Baby Rib Bodysuit dạng thêu, góc nhìn từ phía sau, đường chỉ ngang rõ nét, phong cách thêu thật, dễ thương, có vật trang trí như gấu bông, chăn nhỏ. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024.",
    "Hat": "Vẽ lại thiết kế trên mặt sau mockup mũ dạng thêu, góc nhìn từ phía sau, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng tự nhiên, bối cảnh lifestyle, có vật trang trí nhỏ. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024.",
    "Mug": "Vẽ lại thiết kế trên mockup ly sứ, phong cách tự nhiên, ánh sáng thật, bối cảnh đẹp, có vật trang trí như sách, cây, bàn gỗ. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024."
}

# Backward compatibility
MOCKUP_PROMPTS_EMBROIDERY = MOCKUP_PROMPTS_EMBROIDERY_FRONT

# ===== MOCKUP MODEL PROMPTS =====
# Mockup Print Type with Model - Front - Male
MOCKUP_PROMPTS_PRINT_MODEL_FRONT_MALE = {
    "T-shirt": "Vẽ lại thiết kế trên mặt trước mockup áo T-shirt, phong cách tự nhiên, ánh sáng thật, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hooded": "Vẽ lại thiết kế trên mặt trước mockup áo Hoodie, phong cách tự nhiên, ánh sáng thật, bối cảnh lifestyle, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Sweatshirt": "Vẽ lại thiết kế trên mặt trước mockup áo Sweatshirt, phong cách tự nhiên, ánh sáng mềm, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Baby Rib Bodysuit": "Vẽ lại thiết kế trên mặt trước mockup Baby Rib Bodysuit, phong cách dễ thương, tự nhiên, có vật trang trí như gấu bông, chăn nhỏ. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hat": "Vẽ lại thiết kế trên mặt trước mockup mũ, phong cách tự nhiên, ánh sáng thật, bối cảnh lifestyle, có vật trang trí nhỏ. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Mug": "Vẽ lại thiết kế trên mockup ly sứ, phong cách tự nhiên, ánh sáng thật, bối cảnh đẹp, có vật trang trí như sách, cây, bàn gỗ. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024."
}

# Mockup Print Type with Model - Front - Female
MOCKUP_PROMPTS_PRINT_MODEL_FRONT_FEMALE = {
    "T-shirt": "Vẽ lại thiết kế trên mặt trước mockup áo T-shirt, phong cách tự nhiên, ánh sáng thật, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hooded": "Vẽ lại thiết kế trên mặt trước mockup áo Hoodie, phong cách tự nhiên, ánh sáng thật, bối cảnh lifestyle, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Sweatshirt": "Vẽ lại thiết kế trên mặt trước mockup áo Sweatshirt, phong cách tự nhiên, ánh sáng mềm, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Baby Rib Bodysuit": "Vẽ lại thiết kế trên mặt trước mockup Baby Rib Bodysuit, phong cách dễ thương, tự nhiên, có vật trang trí như gấu bông, chăn nhỏ. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hat": "Vẽ lại thiết kế trên mặt trước mockup mũ, phong cách tự nhiên, ánh sáng thật, bối cảnh lifestyle, có vật trang trí nhỏ. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Mug": "Vẽ lại thiết kế trên mockup ly sứ, phong cách tự nhiên, ánh sáng thật, bối cảnh đẹp, có vật trang trí như sách, cây, bàn gỗ. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024."
}

# Backward compatibility
MOCKUP_PROMPTS_PRINT_MODEL_FRONT = MOCKUP_PROMPTS_PRINT_MODEL_FRONT_MALE

# Mockup Print Type with Model - Back - Male
MOCKUP_PROMPTS_PRINT_MODEL_BACK_MALE = {
    "T-shirt": "Vẽ lại thiết kế trên mặt sau mockup áo T-shirt, góc nhìn từ phía sau, phong cách tự nhiên, ánh sáng thật, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hooded": "Vẽ lại thiết kế trên mặt sau mockup áo Hoodie, góc nhìn từ phía sau, phong cách tự nhiên, ánh sáng thật, bối cảnh lifestyle, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Sweatshirt": "Vẽ lại thiết kế trên mặt sau mockup áo Sweatshirt, góc nhìn từ phía sau, phong cách tự nhiên, ánh sáng mềm, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Baby Rib Bodysuit": "Vẽ lại thiết kế trên mặt sau mockup Baby Rib Bodysuit, góc nhìn từ phía sau, phong cách dễ thương, tự nhiên, có vật trang trí như gấu bông, chăn nhỏ. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hat": "Vẽ lại thiết kế trên mặt sau mockup mũ, góc nhìn từ phía sau, phong cách tự nhiên, ánh sáng thật, bối cảnh lifestyle, có vật trang trí nhỏ. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Mug": "Vẽ lại thiết kế trên mockup ly sứ, phong cách tự nhiên, ánh sáng thật, bối cảnh đẹp, có vật trang trí như sách, cây, bàn gỗ. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024."
}

# Mockup Print Type with Model - Back - Female
MOCKUP_PROMPTS_PRINT_MODEL_BACK_FEMALE = {
    "T-shirt": "Vẽ lại thiết kế trên mặt sau mockup áo T-shirt, góc nhìn từ phía sau, phong cách tự nhiên, ánh sáng thật, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hooded": "Vẽ lại thiết kế trên mặt sau mockup áo Hoodie, góc nhìn từ phía sau, phong cách tự nhiên, ánh sáng thật, bối cảnh lifestyle, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Sweatshirt": "Vẽ lại thiết kế trên mặt sau mockup áo Sweatshirt, góc nhìn từ phía sau, phong cách tự nhiên, ánh sáng mềm, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Baby Rib Bodysuit": "Vẽ lại thiết kế trên mặt sau mockup Baby Rib Bodysuit, góc nhìn từ phía sau, phong cách dễ thương, tự nhiên, có vật trang trí như gấu bông, chăn nhỏ. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hat": "Vẽ lại thiết kế trên mặt sau mockup mũ, góc nhìn từ phía sau, phong cách tự nhiên, ánh sáng thật, bối cảnh lifestyle, có vật trang trí nhỏ. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Mug": "Vẽ lại thiết kế trên mockup ly sứ, phong cách tự nhiên, ánh sáng thật, bối cảnh đẹp, có vật trang trí như sách, cây, bàn gỗ. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024."
}

# Backward compatibility
MOCKUP_PROMPTS_PRINT_MODEL_BACK = MOCKUP_PROMPTS_PRINT_MODEL_BACK_MALE

# Backward compatibility
MOCKUP_PROMPTS_PRINT_MODEL = MOCKUP_PROMPTS_PRINT_MODEL_FRONT

# Mockup Embroidery Type with Model - Front - Male
MOCKUP_PROMPTS_EMBROIDERY_MODEL_FRONT_MALE = {
    "T-shirt": "Vẽ lại thiết kế trên mặt trước mockup áo T-shirt dạng thêu, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng tự nhiên, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hooded": "Vẽ lại thiết kế trên mặt trước mockup áo Hoodie dạng thêu, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng tự nhiên, bối cảnh lifestyle, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Sweatshirt": "Vẽ lại thiết kế trên mặt trước mockup áo Sweatshirt dạng thêu, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng mềm, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Baby Rib Bodysuit": "Vẽ lại thiết kế trên mặt trước mockup Baby Rib Bodysuit dạng thêu, đường chỉ ngang rõ nét, phong cách thêu thật, dễ thương, có vật trang trí như gấu bông, chăn nhỏ. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hat": "Vẽ lại thiết kế trên mặt trước mockup mũ dạng thêu, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng tự nhiên, bối cảnh lifestyle, có vật trang trí nhỏ. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Mug": "Vẽ lại thiết kế trên mockup ly sứ, phong cách tự nhiên, ánh sáng thật, bối cảnh đẹp, có vật trang trí như sách, cây, bàn gỗ. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024."
}

# Mockup Embroidery Type with Model - Front - Female
MOCKUP_PROMPTS_EMBROIDERY_MODEL_FRONT_FEMALE = {
    "T-shirt": "Vẽ lại thiết kế trên mặt trước mockup áo T-shirt dạng thêu, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng tự nhiên, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hooded": "Vẽ lại thiết kế trên mặt trước mockup áo Hoodie dạng thêu, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng tự nhiên, bối cảnh lifestyle, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Sweatshirt": "Vẽ lại thiết kế trên mặt trước mockup áo Sweatshirt dạng thêu, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng mềm, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Baby Rib Bodysuit": "Vẽ lại thiết kế trên mặt trước mockup Baby Rib Bodysuit dạng thêu, đường chỉ ngang rõ nét, phong cách thêu thật, dễ thương, có vật trang trí như gấu bông, chăn nhỏ. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hat": "Vẽ lại thiết kế trên mặt trước mockup mũ dạng thêu, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng tự nhiên, bối cảnh lifestyle, có vật trang trí nhỏ. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Mug": "Vẽ lại thiết kế trên mockup ly sứ, phong cách tự nhiên, ánh sáng thật, bối cảnh đẹp, có vật trang trí như sách, cây, bàn gỗ. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024."
}

# Backward compatibility
MOCKUP_PROMPTS_EMBROIDERY_MODEL_FRONT = MOCKUP_PROMPTS_EMBROIDERY_MODEL_FRONT_MALE

# Mockup Embroidery Type with Model - Back - Male
MOCKUP_PROMPTS_EMBROIDERY_MODEL_BACK_MALE = {
    "T-shirt": "Vẽ lại thiết kế trên mặt sau mockup áo T-shirt dạng thêu, góc nhìn từ phía sau, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng tự nhiên, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hooded": "Vẽ lại thiết kế trên mặt sau mockup áo Hoodie dạng thêu, góc nhìn từ phía sau, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng tự nhiên, bối cảnh lifestyle, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Sweatshirt": "Vẽ lại thiết kế trên mặt sau mockup áo Sweatshirt dạng thêu, góc nhìn từ phía sau, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng mềm, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Baby Rib Bodysuit": "Vẽ lại thiết kế trên mặt sau mockup Baby Rib Bodysuit dạng thêu, góc nhìn từ phía sau, đường chỉ ngang rõ nét, phong cách thêu thật, dễ thương, có vật trang trí như gấu bông, chăn nhỏ. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hat": "Vẽ lại thiết kế trên mặt sau mockup mũ dạng thêu, góc nhìn từ phía sau, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng tự nhiên, bối cảnh lifestyle, có vật trang trí nhỏ. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Mug": "Vẽ lại thiết kế trên mockup ly sứ, phong cách tự nhiên, ánh sáng thật, bối cảnh đẹp, có vật trang trí như sách, cây, bàn gỗ. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024."
}

# Mockup Embroidery Type with Model - Back - Female
MOCKUP_PROMPTS_EMBROIDERY_MODEL_BACK_FEMALE = {
    "T-shirt": "Vẽ lại thiết kế trên mặt sau mockup áo T-shirt dạng thêu, góc nhìn từ phía sau, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng tự nhiên, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hooded": "Vẽ lại thiết kế trên mặt sau mockup áo Hoodie dạng thêu, góc nhìn từ phía sau, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng tự nhiên, bối cảnh lifestyle, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Sweatshirt": "Vẽ lại thiết kế trên mặt sau mockup áo Sweatshirt dạng thêu, góc nhìn từ phía sau, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng mềm, bối cảnh đẹp, có vật trang trí. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Baby Rib Bodysuit": "Vẽ lại thiết kế trên mặt sau mockup Baby Rib Bodysuit dạng thêu, góc nhìn từ phía sau, đường chỉ ngang rõ nét, phong cách thêu thật, dễ thương, có vật trang trí như gấu bông, chăn nhỏ. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hat": "Vẽ lại thiết kế trên mặt sau mockup mũ dạng thêu, góc nhìn từ phía sau, đường chỉ ngang rõ nét, phong cách thêu thật, ánh sáng tự nhiên, bối cảnh lifestyle, có vật trang trí nhỏ. Mockup phù hợp để đăng bán trên Etsy. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Mug": "Vẽ lại thiết kế trên mockup ly sứ, phong cách tự nhiên, ánh sáng thật, bối cảnh đẹp, có vật trang trí như sách, cây, bàn gỗ. Mockup phù hợp để đăng bán trên Etsy. Ảnh kích thước 1024x1024."
}

# Backward compatibility
MOCKUP_PROMPTS_EMBROIDERY_MODEL_BACK = MOCKUP_PROMPTS_EMBROIDERY_MODEL_BACK_MALE

# Backward compatibility
MOCKUP_PROMPTS_EMBROIDERY_MODEL = MOCKUP_PROMPTS_EMBROIDERY_MODEL_FRONT

# ===== TIKTOK SHOP PROMPTS (WHITE BACKGROUND) =====
# TikTok Shop Print Type - Front - Male
MOCKUP_PROMPTS_PRINT_FRONT_MALE_TIKTOK = {
    "T-shirt": "Vẽ lại thiết kế trên mặt trước mockup áo T-shirt, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hooded": "Vẽ lại thiết kế trên mặt trước mockup áo Hoodie, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Sweatshirt": "Vẽ lại thiết kế trên mặt trước mockup áo Sweatshirt, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Baby Rib Bodysuit": "Vẽ lại thiết kế trên mặt trước mockup Baby Rib Bodysuit, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hat": "Vẽ lại thiết kế trên mặt trước mockup mũ, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Mug": "Vẽ lại thiết kế trên mockup ly sứ, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Ảnh kích thước 1024x1024."
}

# TikTok Shop Print Type - Front - Female
MOCKUP_PROMPTS_PRINT_FRONT_FEMALE_TIKTOK = {
    "T-shirt": "Vẽ lại thiết kế trên mặt trước mockup áo T-shirt, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hooded": "Vẽ lại thiết kế trên mặt trước mockup áo Hoodie, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Sweatshirt": "Vẽ lại thiết kế trên mặt trước mockup áo Sweatshirt, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Baby Rib Bodysuit": "Vẽ lại thiết kế trên mặt trước mockup Baby Rib Bodysuit, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hat": "Vẽ lại thiết kế trên mặt trước mockup mũ, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Mug": "Vẽ lại thiết kế trên mockup ly sứ, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Ảnh kích thước 1024x1024."
}

# TikTok Shop Print Type - Back - Male
MOCKUP_PROMPTS_PRINT_BACK_MALE_TIKTOK = {
    "T-shirt": "Vẽ lại thiết kế trên mặt sau mockup áo T-shirt, góc nhìn từ phía sau, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hooded": "Vẽ lại thiết kế trên mặt sau mockup áo Hoodie, góc nhìn từ phía sau, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Sweatshirt": "Vẽ lại thiết kế trên mặt sau mockup áo Sweatshirt, góc nhìn từ phía sau, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Baby Rib Bodysuit": "Vẽ lại thiết kế trên mặt sau mockup Baby Rib Bodysuit, góc nhìn từ phía sau, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hat": "Vẽ lại thiết kế trên mặt sau mockup mũ, góc nhìn từ phía sau, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Có người mẫu nam kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Mug": "Vẽ lại thiết kế trên mockup ly sứ, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Ảnh kích thước 1024x1024."
}

# TikTok Shop Print Type - Back - Female
MOCKUP_PROMPTS_PRINT_BACK_FEMALE_TIKTOK = {
    "T-shirt": "Vẽ lại thiết kế trên mặt sau mockup áo T-shirt, góc nhìn từ phía sau, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hooded": "Vẽ lại thiết kế trên mặt sau mockup áo Hoodie, góc nhìn từ phía sau, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Sweatshirt": "Vẽ lại thiết kế trên mặt sau mockup áo Sweatshirt, góc nhìn từ phía sau, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Baby Rib Bodysuit": "Vẽ lại thiết kế trên mặt sau mockup Baby Rib Bodysuit, góc nhìn từ phía sau, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Hat": "Vẽ lại thiết kế trên mặt sau mockup mũ, góc nhìn từ phía sau, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Có người mẫu nữ kiểu người Âu - Mỹ. Ảnh kích thước 1024x1024.",
    "Mug": "Vẽ lại thiết kế trên mockup ly sứ, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Ảnh kích thước 1024x1024."
}

# TikTok Shop Print Type - Front - No Model
MOCKUP_PROMPTS_PRINT_FRONT_TIKTOK = {
    "T-shirt": "Vẽ lại thiết kế trên mặt trước mockup áo T-shirt, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí, không có người mẫu. Mockup phù hợp để đăng bán trên TikTok Shop. Ảnh kích thước 1024x1024.",
    "Hooded": "Vẽ lại thiết kế trên mặt trước mockup áo Hoodie, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí, không có người mẫu. Mockup phù hợp để đăng bán trên TikTok Shop. Ảnh kích thước 1024x1024.",
    "Sweatshirt": "Vẽ lại thiết kế trên mặt trước mockup áo Sweatshirt, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí, không có người mẫu. Mockup phù hợp để đăng bán trên TikTok Shop. Ảnh kích thước 1024x1024.",
    "Baby Rib Bodysuit": "Vẽ lại thiết kế trên mặt trước mockup Baby Rib Bodysuit, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí, không có người mẫu. Mockup phù hợp để đăng bán trên TikTok Shop. Ảnh kích thước 1024x1024.",
    "Hat": "Vẽ lại thiết kế trên mặt trước mockup mũ, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí, không có người mẫu. Mockup phù hợp để đăng bán trên TikTok Shop. Ảnh kích thước 1024x1024.",
    "Mug": "Vẽ lại thiết kế trên mockup ly sứ, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Ảnh kích thước 1024x1024."
}

# TikTok Shop Print Type - Back - No Model
MOCKUP_PROMPTS_PRINT_BACK_TIKTOK = {
    "T-shirt": "Vẽ lại thiết kế trên mặt sau mockup áo T-shirt, góc nhìn từ phía sau, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí, không có người mẫu. Mockup phù hợp để đăng bán trên TikTok Shop. Ảnh kích thước 1024x1024.",
    "Hooded": "Vẽ lại thiết kế trên mặt sau mockup áo Hoodie, góc nhìn từ phía sau, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí, không có người mẫu. Mockup phù hợp để đăng bán trên TikTok Shop. Ảnh kích thước 1024x1024.",
    "Sweatshirt": "Vẽ lại thiết kế trên mặt sau mockup áo Sweatshirt, góc nhìn từ phía sau, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí, không có người mẫu. Mockup phù hợp để đăng bán trên TikTok Shop. Ảnh kích thước 1024x1024.",
    "Baby Rib Bodysuit": "Vẽ lại thiết kế trên mặt sau mockup Baby Rib Bodysuit, góc nhìn từ phía sau, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí, không có người mẫu. Mockup phù hợp để đăng bán trên TikTok Shop. Ảnh kích thước 1024x1024.",
    "Hat": "Vẽ lại thiết kế trên mặt sau mockup mũ, góc nhìn từ phía sau, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí, không có người mẫu. Mockup phù hợp để đăng bán trên TikTok Shop. Ảnh kích thước 1024x1024.",
    "Mug": "Vẽ lại thiết kế trên mockup ly sứ, nền trắng hoàn toàn, ánh sáng đều, không có vật trang trí. Mockup phù hợp để đăng bán trên TikTok Shop. Ảnh kích thước 1024x1024."
}

from api_client import fetch_mockup_templates, upload_image_to_imgbb, render_mockup
from upscayl_processor import UpscaylProcessor
from gemini_client import GeminiClient
from photoroom_client import PhotoRoomClient
from user_manager import UserManager
from login_dialog import LoginDialog
from account_tab import AccountTab

# <<< NEW >>>
def get_base_path():
    """Get the base path for the application, works for both development and PyInstaller builds."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Running in a PyInstaller bundle
        return Path(sys._MEIPASS)
    else:
        # Running in a normal development environment
        return Path(__file__).parent

def get_cache_path():
    """Get the cache directory path for storing mockup templates."""
    import tempfile
    
    # Try to use user's home directory first, fallback to temp directory
    try:
        home_dir = Path.home()
        cache_dir = home_dir / "JEGDesignExtract" / "mockup_cache"
    except:
        cache_dir = Path(tempfile.gettempdir()) / "JEGDesignExtract" / "mockup_cache"
    
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir

# --- Upscayl Configuration ---
# Root directory containing the Upscayl executable and models
UPSCARYL_CORE_DIR = get_base_path() / "upscayl_core"
# Path to the directory containing .bin and .param models
UPSCARYL_MODELS_PATH = UPSCARYL_CORE_DIR / "models"
# Path to the upscayl-ncnn executable
UPSCARYL_EXEC_PATH = UPSCARYL_CORE_DIR / "bin" / ("upscayl-ncnn.exe" if platform.system() == "Windows" else "upscayl-ncnn")

class MockupTemplateCache:
    """Manages caching of mockup templates for faster loading."""
    
    def __init__(self):
        self.cache_dir = get_cache_path()
        self.cache_index_file = self.cache_dir / "cache_index.json"
        self.cache_index = self._load_cache_index()
    
    def _load_cache_index(self):
        """Load the cache index from file."""
        if self.cache_index_file.exists():
            try:
                with open(self.cache_index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading cache index: {e}")
        return {}
    
    def _save_cache_index(self):
        """Save the cache index to file."""
        try:
            with open(self.cache_index_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache_index, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving cache index: {e}")
    
    def get_cached_template(self, template_id):
        """Get a cached template image if it exists."""
        if template_id in self.cache_index:
            cache_info = self.cache_index[template_id]
            cache_file = self.cache_dir / cache_info['filename']
            if cache_file.exists():
                try:
                    return Image.open(cache_file)
                except Exception as e:
                    print(f"Error loading cached template {template_id}: {e}")
                    # Remove invalid cache entry
                    del self.cache_index[template_id]
                    if cache_file.exists():
                        cache_file.unlink()
        return None
    
    def cache_template(self, template_id, template_data, image_data):
        """Cache a template image."""
        try:
            # Create filename based on template ID
            filename = f"{template_id}.png"
            cache_file = self.cache_dir / filename
            
            # Save image to cache
            image = Image.open(BytesIO(image_data))
            image.save(cache_file, 'PNG', dpi=(300, 300))
            
            # Update cache index
            self.cache_index[template_id] = {
                'filename': filename,
                'timestamp': datetime.now().isoformat(),
                'size': cache_file.stat().st_size
            }
            self._save_cache_index()
            
            print(f"Cached template {template_id}")
            return True
        except Exception as e:
            print(f"Error caching template {template_id}: {e}")
            return False
    
    def clear_cache(self):
        """Clear all cached templates."""
        try:
            for cache_info in self.cache_index.values():
                cache_file = self.cache_dir / cache_info['filename']
                if cache_file.exists():
                    cache_file.unlink()
            
            self.cache_index.clear()
            self._save_cache_index()
            print("Cache cleared")
        except Exception as e:
            print(f"Error clearing cache: {e}")

class ImageProcessor:
    """
    Handles the core image processing tasks like background removal and upscaling.
    Now includes mechanisms for cancellation and progress reporting.
    """
    
    def __init__(self, log_callback=None, progress_callback=None, cancel_event=None):
        self.log_callback = log_callback
        self.progress_callback = progress_callback
        self.cancel_event = cancel_event or threading.Event()

    def log(self, msg):
        """Log processing steps"""
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        log_msg = f"{timestamp} {msg}"
        print(log_msg)
        if self.log_callback:
            self.log_callback(log_msg)

    def _check_cancel(self):
        """Checks if cancellation has been requested and raises an exception if so."""
        if self.cancel_event.is_set():
            raise UserWarning("Processing cancelled by user.")

    

    def _run_ai_upscale(self, rgba_img, upscayl_model, scale_factor):
        """
        Runs the Upscayl AI process, now with cancellation support.
        """
        self.log(f"   - Starting AI Upscale (Model: {upscayl_model}, Scale: {scale_factor}x)...")
        self._check_cancel()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            temp_input_path = temp_dir_path / "temp_input.png"
            temp_output_path = temp_dir_path / "temp_output.png"

            # Saving input image (OpenCV BGRA format) to temp file
            cv2.imwrite(str(temp_input_path), rgba_img)
            
            # Construct the command for the subprocess
            command = [
                str(UPSCARYL_EXEC_PATH),
                "-i", str(temp_input_path),
                "-o", str(temp_output_path),
                "-s", str(scale_factor),
                "-m", str(UPSCARYL_MODELS_PATH),
                "-f", "png",
                "-n", upscayl_model
            ]

            try:
                # Use subprocess.run for simplicity if streaming output isn't critical
                # For streaming, Popen is still good.
                # Fix Windows encoding issues
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                    encoding='utf-8',  # Force UTF-8 encoding
                    errors='replace',  # Replace invalid characters
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0  # Hide console on Windows
                )
                
                while True:
                    self._check_cancel()
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        self.log(f"     [Upscayl]: {output.strip()}")
                
                if process.returncode != 0:
                    raise RuntimeError(f"Upscayl process failed with code {process.returncode}")

            except FileNotFoundError:
                self.log(f"❌ ERROR: Upscayl executable not found at: {UPSCARYL_EXEC_PATH}")
                raise
            except Exception as e:
                self.log(f"❌ Error during AI Upscale: {e}")
                raise

            if not temp_output_path.exists():
                self.log("❌ ERROR: Upscayl did not generate an output file.")
                raise FileNotFoundError("Upscayl output file not found.")
                
            upscaled_image = cv2.imread(str(temp_output_path), cv2.IMREAD_UNCHANGED)
            self.log("   - ✅ AI Upscale complete.")
            return upscaled_image

    def _place_on_final_canvas(self, rgba_img, target_size):
        """
        Resizes and places the image onto a transparent canvas with anti-aliasing.
        """
        self.log(f"   - Placing image onto {target_size[0]}x{target_size[1]}px canvas với anti-aliasing...")
        self._check_cancel()
        pil_img = Image.fromarray(cv2.cvtColor(rgba_img, cv2.COLOR_BGRA2RGBA))

        # Keep aspect ratio, resize to fit target_size with high-quality resampling
        pil_img.thumbnail(target_size, resample=Image.Resampling.LANCZOS)

        final_canvas = Image.new("RGBA", target_size, (255, 255, 255, 0))
        x = (target_size[0] - pil_img.width) // 2
        y = (target_size[1] - pil_img.height) // 2
        
        # Use alpha composite for better blending instead of paste
        temp_canvas = Image.new("RGBA", target_size, (255, 255, 255, 0))
        temp_canvas.paste(pil_img, (x, y))
        final_canvas = Image.alpha_composite(final_canvas, temp_canvas)
        
        self.log(f"   - ✅ Image placed on canvas với smooth edges.")
        return cv2.cvtColor(np.array(final_canvas), cv2.COLOR_RGBA2BGRA)
    


class ImageItem:
    def __init__(self, file_path):
        self.file_path = file_path
        self.filename = os.path.basename(file_path)
        self.original_image = None
        self.processed_image = None
        self.crop_coordinates = None  # (x1, y1, x2, y2)
        self.thumbnail = None
        self.status = "pending"  # pending, processing, completed, error
        self.processed_size = None  # (width, height) of last processed output
        self.processed_model = None
        self.selected_for_download = True  # For download selection (default: selected)

        # --- NEW: Cache Invalidation Logic ---
        self.last_processed_params = {
            'crop': None,
            'model': None,
            'size': None
        }

        # --- NEW: GIF Animation ---
        self.gif_frames = []
        self.gif_label = None
        self.gif_animation_job = None
        self.gif_frame_index = 0

class JEGDesignExtractGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JEG Design Studio v2.2.0")
        
        
        # Platform-specific window configuration
        if platform.system() == "Windows":
            self.root.geometry("1400x900")
            # Windows specific styling - use safer configuration
            try:
                self.root.option_add('*TCombobox*Listbox.selectBackground', '#4a90e2')
                # Don't set global font here, will be set per widget
            except:
                pass
            # Windows-specific DPI awareness (do this after basic setup)
            try:
                import ctypes
                # Use more conservative DPI setting
                ctypes.windll.user32.SetProcessDPIAware()
            except:
                pass
        elif platform.system() == "Darwin":  # macOS
            self.root.geometry("1400x900")
            # macOS specific styling
            try:
                # Don't set global font here, will be set per widget
                pass
            except:
                pass
        else:
            self.root.geometry("1400x900")
            # Linux/Generic styling
            try:
                # Don't set global font here, will be set per widget
                pass
            except:
                pass
            
        self.root.resizable(True, True)
        
        # Configure dark theme colors with platform-specific adjustments
        if platform.system() == "Windows":
            self.colors = {
                'bg_dark': '#2E2E2E',
                'bg_medium': '#3C3C3C',
                'bg_light': '#4A4A4A',
                'accent': '#0078D4',  # Windows accent blue
                'text_white': '#FFFFFF',
                'text_gray': '#AAAAAA',
                'button_bg': '#0078D4',
                'button_hover': '#106ebe',
                'error': '#DC3545'  # Red color for error/cancel button
            }
        else:
            self.colors = {
                'bg_dark': '#2E2E2E',
                'bg_medium': '#3C3C3C',
                'bg_light': '#4A4A4A',
                'accent': '#007AFF',  # System blue for selection
                'text_white': '#FFFFFF',
                'text_gray': '#AAAAAA',
                'button_bg': '#007AFF',
                'button_hover': '#005cbf',
                'error': '#DC3545'  # Red color for error/cancel button
            }
        
        # Configure root
        self.root.configure(bg=self.colors['bg_dark'])
        
        # Variables
        self.image_items = []
        self.current_image_item = None
        self.selection_start = None
        self.selection_end = None
        self.selection_rect = None
        self.is_processing = False
        self.cancel_event = threading.Event()
        
        # Mockup tab variables
        self.mockup_image_items = []
        self.mockup_current_image_item = None
        self.mockup_selection_start = None
        self.mockup_selection_end = None
        self.mockup_selection_rect = None
        self.mockup_is_processing = False
        
        # --- NEW: Cache Invalidation Logic ---
        # NOTE: This seems to be from the 'extract' tab, might need review if it applies to 'redesign'
        self.last_processed_params = {
            'crop': None,
            'model': None,
            'size': None
        }

        # --- NEW: GIF Animation ---
        self.gif_frames = []
        self.gif_label = None
        self.gif_animation_job = None
        self.gif_frame_index = 0

        self._create_button_images()
        
        # Canvas display info for coordinate conversion
        self.canvas_image_info = {
            'scale_factor': 1.0,
            'offset_x': 0,
            'offset_y': 0,
            'display_width': 0,
            'display_height': 0
        }
        
        # Initialize processor with log callback and cancel event
        self.upscale_cancel_event = threading.Event()
        self.processor = ImageProcessor(
            log_callback=self.add_log,
            cancel_event=self.upscale_cancel_event
        )
        
        # Initialize mockup template cache
        self.mockup_cache = MockupTemplateCache()
        
        # Data and state management
        self.image_paths = []
        
        # Initialize User Manager (must be before setup_ui)
        self.user_manager = UserManager()
        
        self.setup_styles()
        self.setup_ui()
        self.load_gif()
        self.update_processed_list()
        self.check_upscayl_resources()
        
        # Log cache status
        cache_count = len(self.mockup_cache.cache_index)
        if cache_count > 0:
            self.add_log(f"📦 Mockup template cache: {cache_count} templates available")
        else:
            self.add_log("📦 Mockup template cache: empty (templates will be downloaded on first use)")
        
        # Bind cleanup on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Log initial settings
        self.add_log("🎨 JEG Design v2.1.0 (AI Upscale Edition) ready!")
        
        # Check authentication status and show welcome screen if needed
        # TEMPORARILY DISABLED - Skip authentication check
        # if not self.is_authenticated:
        #     self.root.after(500, self.show_welcome_screen)
        target_size = self.parse_size_from_dropdown()
        self.add_log(f"📐 Default output size: {target_size[0]} x {target_size[1]} px @ 300 DPI")
        self.add_log("🤖 AI Model: digital-art-4x (optimized for design/artwork)")
        self.add_log("📦 Batch Mode: disabled (single image processing)")
        self.add_log("💡 Tip: Enable Batch Mode to process multiple images at once")
        self.add_log("💾 Download: Use checkboxes in 'Processed Results' to select images for saving")
        self.add_log("🖱️ Left-click: Select design area | Right-click: Paste from clipboard")
        self.add_log("📁 Use 'Browse...' button to add images")
        self.add_log("🔄 Redesign: Results are stored in memory - use 'Save Results' to save selected images")
        self.add_log("🔄 Redesign: Cache is invalidated when mode/model changes, output size only resizes")
        
        self.selection_rect_id = None
        self.selection_coords = {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 0}
        self.upscale_active_item_frame = None

        self.zoom_level = 1.0
        self.pan_start_x = 0


        # --- Cache ---
        # Cache for upscaled images from the 'extract' feature
        self.last_upscaled_data = None # This will store the raw image data from upscayl

        self.total_processed_var = tk.StringVar(self.root, "Tổng số đã xử lý: 0")
        self.current_status_var = tk.StringVar(self.root, "Trạng thái: Sẵn sàng")
        self.last_upscaled_data = None # This will store the raw image data from upscayl
  
        self.upscayl_processor = UpscaylProcessor(log_callback=self.add_log, cancel_event=self.cancel_event)
        
        # Clean up any existing temporary items on startup
        self.cleanup_temporary_items_on_startup()
        
        # Clear any existing session and always require login
        self.user_manager.logout()  # Clear any existing session
        self.root.after(100, self.show_login_dialog)

    def _create_button_images(self):
        """Pre-render all button images for normal and selected states."""
        self.button_images = {}
        button_config = {
            "width": 200, "height": 45, "radius": 8,
            "font_size": 12, "text_padx": 20,
            "color_normal": "#3A3A3A",
            "color_selected": "#555555",
            "text_color": "#FFFFFF"
        }

        tabs = ["Extract design", "Mockup", "Up scale", "Video gen", "Account"]
        keys = ["extract", "mockup", "upscale", "video_gen", "account"]

        for key, text in zip(keys, tabs):
            self.button_images[key] = {
                'normal': self._create_single_button_image(text=text, **button_config),
                'selected': self._create_single_button_image(text=text, color_bg=button_config['color_selected'], **button_config)
            }

    def _create_single_button_image(self, text, width, height, radius, font_size, text_padx, color_normal, color_selected, text_color, color_bg=None):
        """Creates a single PhotoImage for a button state."""
        if color_bg is None:
            color_bg = color_normal
        
        try:
            font = ImageFont.truetype("Arial.ttf", font_size)
        except IOError:
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except IOError:
                font = ImageFont.load_default()

        image = Image.new("RGBA", (width, height), (255, 255, 255, 0)) # Transparent background
        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle((0, 0, width, height), radius, fill=color_bg)
        
        text_y = (height - font.getbbox(text)[3] - font.getbbox(text)[1]) / 2
        draw.text((text_padx, text_y), text, font=font, fill=text_color)
        
        return ImageTk.PhotoImage(image)
        
    def setup_styles(self):
        """Configure ttk styles for dark theme"""
        style = ttk.Style()
        
        # Platform-specific fonts with fallbacks
        try:
            if platform.system() == "Windows":
                # Try Windows fonts with fallbacks
                try:
                    import tkinter.font as tkFont
                    # Test if Segoe UI is available
                    test_font = tkFont.Font(family='Segoe UI', size=9)
                    default_font = ('Segoe UI', 9)
                    title_font = ('Segoe UI', 12, 'bold')
                    label_font = ('Segoe UI', 9)
                except:
                    # Fallback to system default
                    default_font = ('TkDefaultFont', 9)
                    title_font = ('TkDefaultFont', 12, 'bold')
                    label_font = ('TkDefaultFont', 9)
            elif platform.system() == "Darwin":  # macOS
                default_font = ('SF Pro Display', 13)
                title_font = ('SF Pro Display', 16, 'bold')
                label_font = ('SF Pro Display', 13)
            else:  # Linux/Other
                default_font = ('TkDefaultFont', 10)
                title_font = ('TkDefaultFont', 14, 'bold')
                label_font = ('TkDefaultFont', 10)
        except:
            # Ultimate fallback
            default_font = ('TkDefaultFont', 10)
            title_font = ('TkDefaultFont', 12, 'bold')
            label_font = ('TkDefaultFont', 10)
        
        # Configure styles with safe font handling
        try:
            style.configure('Sidebar.TFrame', background=self.colors['bg_dark'])
            style.configure('Main.TFrame', background=self.colors['bg_medium'])
            style.configure('Dark.TFrame', background=self.colors['bg_dark'])
            style.configure('Panel.TFrame', background=self.colors['bg_light'])
            
            style.configure('Sidebar.TLabel', 
                           background=self.colors['bg_dark'],
                           foreground=self.colors['text_white'],
                           font=label_font)
            style.configure('Title.TLabel',
                           background=self.colors['bg_medium'],
                           foreground=self.colors['text_white'],
                           font=title_font)
            style.configure('Panel.TLabel',
                           background=self.colors['bg_light'],
                           foreground=self.colors['text_white'],
                           font=label_font)
            
            style.configure('Sidebar.TButton',
                           background=self.colors['bg_light'],
                           foreground=self.colors['text_white'],
                           font=default_font)
            style.configure('Active.TButton',
                           background=self.colors['accent'],
                           foreground=self.colors['text_white'],
                           font=default_font)
        except Exception as e:
            # Fallback to system defaults if font configuration fails
            print(f"Warning: Could not configure custom fonts: {e}")
            style.configure('Sidebar.TFrame', background=self.colors['bg_dark'])
            style.configure('Main.TFrame', background=self.colors['bg_medium'])
            style.configure('Dark.TFrame', background=self.colors['bg_dark'])
            style.configure('Panel.TFrame', background=self.colors['bg_light'])
        
    def setup_ui(self):
        # Main container
        main_container = Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar on the left
        self.create_sidebar(main_container)

        # Content area on the right, which will hold the different pages
        content_area = Frame(main_container, bg=self.colors['bg_medium'])
        content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        content_area.grid_rowconfigure(0, weight=1)
        content_area.grid_columnconfigure(0, weight=1)

        self.pages = {}
        page_names = ["extract", "mockup", "upscale", "video_gen", "account"]
        for name in page_names:
            page = Frame(content_area, bg=self.colors['bg_medium'])
            page.grid(row=0, column=0, sticky='nsew')
            self.pages[name] = page
        
        # The original UI is now the 'extract' page
        self.create_main_area(self.pages["extract"])
        
        # Create the UI for the Mockup tab
        self.create_mockup_ui(self.pages["mockup"])
        
        # Create the UI for the Upscale tab
        self.create_upscale_ui(self.pages["upscale"])
        
        # Create the UI for the Video Gen tab
        self.create_video_gen_ui(self.pages["video_gen"])
        
        # Create the UI for the Account tab
        self.create_account_ui(self.pages["account"])
        

        # Add placeholder content for the other pages
        # for name in ["mockup"]:
        #     label = tk.Label(self.pages[name], text="Đang phát triển",
        #                      font=("Arial", 18), bg=self.colors['bg_medium'], fg=self.colors['text_white'])
        #     label.pack(fill=tk.BOTH, expand=True)
            
        # Show the default page
        self.show_page("extract")
        
    def create_upscale_ui(self, parent):
        """Create the redesigned UI for the Upscale tab, mimicking the Extract tab layout."""
        # This function now populates the given 'parent' frame
        main_area = Frame(parent, bg=self.colors['bg_medium'])
        main_area.pack(fill=tk.BOTH, expand=True)
        
        # Main content panels (expanded to fill more space)
        self.create_upscale_content_panels(main_area)
        
        # Bottom section
        self.create_upscale_bottom_section(main_area)
        
        # Footer
        self.create_upscale_footer(main_area)
        
    def create_upscale_content_panels(self, parent):
        """Create main content panels for Upscale tab using a grid layout for equal sizing."""
        # Initialize gallery data structures and variables
        self.upscale_original_gallery_items = []
        self.upscale_processed_gallery_items = []
        self.upscale_batch_mode_var = tk.BooleanVar(value=False)
        self.upscale_active_item_frame = None
        
        # Initialize upscale-specific variables
        self.upscale_image_path = None
        self.upscale_original_image = None
        self.upscale_processed_image = None
        self.upscale_tk_original = None
        self.upscale_tk_processed = None
        
        content_frame = Frame(parent, bg=self.colors['bg_medium'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 10))

        # Configure the grid to have two equally sized columns
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left panel - Original Image
        left_panel = Frame(content_frame, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        tk.Label(left_panel, text="Original Image (Select for Upscale)",
                bg=self.colors['bg_light'], fg=self.colors['text_white'],
                font=('Arial', 12, 'bold'), pady=5).pack(fill=tk.X)
        
        self.upscale_original_canvas = Canvas(left_panel, bg='black')
        self.upscale_original_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Bind events for image interaction
        self.upscale_original_canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Right-click: Context menu for paste and browse
        self.upscale_original_canvas.bind("<Button-3>", self.upscale_on_right_click)
        
        # Visual feedback
        self.upscale_original_canvas.configure(cursor="crosshair")
        
        # Right panel - Upscaled Result
        right_panel = Frame(content_frame, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        right_header = Frame(right_panel, bg=self.colors['bg_light'])
        right_header.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(right_header, text="Upscaled Result",
                bg=self.colors['bg_light'], fg=self.colors['text_white'],
                font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        # Canvas for upscaled result
        self.upscale_processed_canvas = Canvas(right_panel, bg='white')
        self.upscale_processed_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Progress bar and status label UI (similar to extract tab)
        self.upscale_progress_frame = Frame(right_panel, bg=self.colors['bg_light'])
        
        self.upscale_progress_label = tk.Label(self.upscale_progress_frame, text="Processing...",
                                      bg=self.colors['bg_light'], fg=self.colors['text_white'],
                                      font=('Arial', 10, 'italic'))

    def create_upscale_bottom_section(self, parent):
        """Create bottom section with dual image lists and upscale options (no activity log)"""
        bottom_frame = Frame(parent, bg=self.colors['bg_medium'], height=300)
        bottom_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        bottom_frame.pack_propagate(False)
        
        # Left side: Original Images + Processed Results
        images_container = Frame(bottom_frame, bg=self.colors['bg_medium'])
        images_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Original Images (Left)
        original_frame = Frame(images_container, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1)
        original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Header with title and buttons
        original_header = Frame(original_frame, bg=self.colors['bg_light'])
        original_header.pack(fill=tk.X, padx=10, pady=(5, 0))
        
        tk.Label(original_header, text="Original Images",
                bg=self.colors['bg_light'], fg=self.colors['text_white'],
                font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        # Action buttons
        btn_frame = Frame(original_header, bg=self.colors['bg_light'])
        btn_frame.pack(side=tk.RIGHT)
        
        tk.Button(btn_frame, text="Browse...", 
                 bg='#e0e0e0', fg='#000000',
                 relief=tk.FLAT, bd=0, padx=10, pady=3,
                 font=('Arial', 9, 'bold'),
                 highlightbackground='#cccccc',
                 command=self.browse_upscale_image).pack(side=tk.LEFT, padx=(5, 2))
        tk.Button(btn_frame, text="Clear All",
                 bg='#e0e0e0', fg='#000000',
                 relief=tk.FLAT, bd=0, padx=10, pady=3,
                 font=('Arial', 9, 'bold'),
                 highlightbackground='#cccccc',
                 command=self.clear_upscale_widgets).pack(side=tk.LEFT, padx=(2, 5))
        
        # Scrollable original image list
        original_scroll_frame = Frame(original_frame, bg=self.colors['bg_light'])
        original_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Container for original image list (scrollable frame instead of listbox)
        self.upscale_list_container = Frame(original_scroll_frame, bg=self.colors['bg_dark'])
        self.upscale_list_container.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable area for upscale images
        self.upscale_canvas = Canvas(self.upscale_list_container, bg=self.colors['bg_dark'])
        self.upscale_scrollbar = Scrollbar(self.upscale_list_container, orient="vertical", command=self.upscale_canvas.yview)
        self.upscale_scrollable_frame = Frame(self.upscale_canvas, bg=self.colors['bg_dark'])
        
        self.upscale_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.upscale_canvas.configure(scrollregion=self.upscale_canvas.bbox("all"))
        )
        
        self.upscale_canvas.create_window((0, 0), window=self.upscale_scrollable_frame, anchor="nw")
        self.upscale_canvas.configure(yscrollcommand=self.upscale_scrollbar.set)
        
        self.upscale_canvas.pack(side="left", fill="both", expand=True)
        self.upscale_scrollbar.pack(side="right", fill="y")
        
        # Processed Results (Right)
        processed_frame = Frame(images_container, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1)
        processed_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Header with download controls
        processed_header = Frame(processed_frame, bg=self.colors['bg_light'])
        processed_header.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(processed_header, text="Processed Results",
                bg=self.colors['bg_light'], fg=self.colors['text_white'],
                font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        # Download controls
        download_controls = Frame(processed_header, bg=self.colors['bg_light'])
        download_controls.pack(side=tk.RIGHT)
        
        tk.Button(download_controls, text="All", 
                 bg='#e0e0e0', fg='#000000',
                 relief=tk.FLAT, bd=0, padx=10, pady=3,
                 font=('Arial', 9, 'bold'),
                 highlightbackground='#cccccc',
                 command=lambda: self.toggle_upscale_checkboxes(True)).pack(side=tk.LEFT, padx=(5, 2))
        
        tk.Button(download_controls, text="None", 
                 bg='#e0e0e0', fg='#000000',
                 relief=tk.FLAT, bd=0, padx=10, pady=3,
                 font=('Arial', 9, 'bold'),
                 highlightbackground='#cccccc',
                 command=lambda: self.toggle_upscale_checkboxes(False)).pack(side=tk.LEFT, padx=(2, 5))
        
        # Separator
        separator = Frame(download_controls, bg='#666666', width=1, height=15)
        separator.pack(side=tk.LEFT, padx=5)
        
        # Save Results button
        tk.Button(download_controls, text="Save Results",
                 bg='#90ee90', fg='#000000',
                 relief=tk.FLAT, bd=0, padx=10, pady=3,
                 font=('Arial', 9, 'bold'),
                 highlightbackground='#cccccc',
                 command=self.save_selected_upscaled).pack(side=tk.LEFT, padx=(5, 5))
        
        # Scrollable processed results list
        self.upscale_processed_scroll_frame = Frame(processed_frame, bg=self.colors['bg_light'])
        self.upscale_processed_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # This will be populated dynamically
        self.upscale_processed_list_container = Frame(self.upscale_processed_scroll_frame, bg=self.colors['bg_dark'])
        self.upscale_processed_list_container.pack(fill=tk.BOTH, expand=True)
        
        # Right side - Upscale Options (replaces Activity Log)
        right_bottom = Frame(bottom_frame, bg=self.colors['bg_medium'])
        right_bottom.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Upscale Options Panel
        options_panel = Frame(right_bottom, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1, width=400)
        options_panel.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        options_panel.pack_propagate(False)
        
        # Options content frame
        options_content = Frame(options_panel, bg=self.colors['bg_light'])
        options_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Row 1: AI Model
        model_row = Frame(options_content, bg=self.colors['bg_light'])
        model_row.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(model_row, text="AI Model:",
                bg=self.colors['bg_light'], fg=self.colors['text_white'],
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.upscale_model_var = tk.StringVar(value="digital-art-4x")
        model_options = [
            "digital-art-4x",
            "high-fidelity-4x", 
            "real-esrgan-4x",
            "ultrasharp-4x"
        ]
        
        self.upscale_model_dropdown = ttk.Combobox(model_row, textvariable=self.upscale_model_var,
                                         values=model_options, state="readonly", width=15,
                                         font=('Arial', 10))
        self.upscale_model_dropdown.pack(side=tk.RIGHT)
        
        # Row 2: Scale Factor
        scale_row = Frame(options_content, bg=self.colors['bg_light'])
        scale_row.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(scale_row, text="Scale Factor:",
                bg=self.colors['bg_light'], fg=self.colors['text_white'],
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.upscale_scale_var = tk.StringVar(value="4x")
        scale_options = ["2x", "3x", "4x", "6x", "8x"]
        
        self.upscale_scale_dropdown = ttk.Combobox(scale_row, textvariable=self.upscale_scale_var,
                                         values=scale_options, state="readonly", width=15,
                                         font=('Arial', 10))
        self.upscale_scale_dropdown.pack(side=tk.RIGHT)
        
        # Processing
        processing_frame = Frame(right_bottom, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1, height=80)
        processing_frame.pack(fill=tk.X)
        processing_frame.pack_propagate(False)
        
        # Progress bar
        self.upscale_progressbar = ttk.Progressbar(processing_frame, mode='indeterminate')
        self.upscale_progressbar.pack(fill=tk.X, padx=20, pady=(10, 5))
        
        # Upscale button
        self.process_upscale_btn = tk.Button(processing_frame, text="Upscale Image",
                                    bg='#90ee90', fg='#000000',
                                    font=('Arial', 11, 'bold'),
                                    relief=tk.FLAT, bd=0,
                                    pady=5, command=self.process_upscale_image)
        self.process_upscale_btn.pack(fill=tk.X, padx=20, pady=(0, 10))
        
    def create_upscale_footer(self, parent):
        """Create footer with copyright for Upscale tab"""
        footer = Frame(parent, bg=self.colors['bg_medium'], height=25)
        footer.pack(fill=tk.X, padx=20, pady=(0, 10))
        footer.pack_propagate(False)
        
        # Copyright label
        copyright_label = tk.Label(footer, text="Copyright 2025 © JEG Technology",
                                  bg=self.colors['bg_medium'],
                                  fg=self.colors['text_gray'],
                                  font=('Arial', 9, 'italic'))
        copyright_label.pack(side=tk.LEFT, anchor='w')

    def clear_upscale_widgets(self):
        """Clears all widgets and data in the upscale tab."""
        # Clear variables
        self.upscale_image_path = None
        self.upscale_original_image = None
        self.upscale_processed_image = None
        self.upscale_tk_original = None
        self.upscale_tk_processed = None

        # Clear canvases
        if hasattr(self, 'upscale_original_canvas'):
            self.upscale_original_canvas.delete("all")
        if hasattr(self, 'upscale_processed_canvas'):
            self.upscale_processed_canvas.delete("all")
        
        # Clear original images scrollable frame
        if hasattr(self, 'upscale_scrollable_frame'):
            for widget in self.upscale_scrollable_frame.winfo_children():
                widget.destroy()
        
        # Clear processed results container
        if hasattr(self, 'upscale_processed_list_container'):
            for widget in self.upscale_processed_list_container.winfo_children():
                widget.destroy()
                
        # Clear gallery lists
        if hasattr(self, 'upscale_original_gallery_items'):
            self.upscale_original_gallery_items.clear()
        if hasattr(self, 'upscale_processed_gallery_items'):
            self.upscale_processed_gallery_items.clear()
                
    def on_upscale_image_select(self, event):
        """Handle selection of image in upscale - deprecated since we use click handlers now"""
        # This function is no longer used since we switched to scrollable frame with click handlers
        pass
            
    def upscale_on_right_click(self, event):
        """Handle right-click on upscale canvas for context menu"""
        # Create context menu
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="Paste Image from Clipboard", command=self.upscale_paste_from_clipboard)
        context_menu.add_separator()
        context_menu.add_command(label="Browse Files...", command=self.browse_upscale_image)
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    def upscale_paste_from_clipboard(self):
        """Paste image from clipboard for upscale"""
        try:
            # Try to get image from clipboard using PIL
            from PIL import ImageGrab
            image = ImageGrab.grabclipboard()
            if image:
                # Save to temporary file
                import tempfile
                temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                image.save(temp_file.name)
                temp_file.close()
                
                # Add to upscale gallery and display
                self.upscale_add_image_files([temp_file.name])
                self.add_upscale_log("📋 Pasted image from clipboard")
                # Auto-select the pasted image
                self.upscale_auto_select_pasted_image(temp_file.name)
                return
            
            # Try to get file path from clipboard
            try:
                clipboard_data = self.root.clipboard_get()
                if os.path.exists(clipboard_data):
                    if clipboard_data.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                        self.upscale_add_image_files([clipboard_data])
                        self.add_upscale_log(f"📋 Pasted image from clipboard: {os.path.basename(clipboard_data)}")
                        self.upscale_auto_select_pasted_image(clipboard_data)
                        return
            except tk.TclError:
                pass
                
            self.add_upscale_log("❌ No valid image found in clipboard")
            
        except Exception as e:
            self.add_upscale_log(f"❌ Error pasting from clipboard: {str(e)}")
    
    def upscale_add_image_files(self, file_paths):
        """Add image files to upscale gallery"""
        for path in file_paths:
            try:
                image_data = cv2.imread(path, cv2.IMREAD_UNCHANGED)
                if image_data is None:
                    self.add_upscale_log(f"   -> Failed to read {os.path.basename(path)}")
                    continue

                # Add to gallery
                self._add_to_upscale_gallery(self.upscale_original_gallery_items, path)
                self.add_upscale_log(f"Loaded: {os.path.basename(path)}")
                
                # If it's the first image, display it
                if len(self.upscale_original_gallery_items) == 1:
                    self.upscale_image_path = path
                    self.upscale_original_image = image_data
                    self._display_image_in_widget(self.upscale_original_image, self.upscale_original_canvas, "original")

            except Exception as e:
                self.add_upscale_log(f"Error loading {os.path.basename(path)}: {e}")
    
    def upscale_auto_select_pasted_image(self, file_path):
        """Auto-select the pasted image by triggering click handler"""
        try:
            # Simply trigger the click handler to display the image
            self.upscale_on_item_click(file_path)
        except Exception as e:
            print(f"Error auto-selecting pasted image: {e}")
            
    def upscale_on_item_click(self, image_path):
        """Handle clicking on upscale item to view"""
        try:
            if os.path.exists(image_path):
                # Load and display the image
                image_data = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
                if image_data is not None:
                    self.upscale_image_path = image_path
                    self.upscale_original_image = image_data
                    self._display_image_in_widget(image_data, self.upscale_original_canvas, "original")
                    self.add_upscale_log(f"📋 Viewing: {os.path.basename(image_path)}")
                    
                    # Clear processed view since we're viewing a different source
                    self.upscale_processed_canvas.delete("all")
                    self.upscale_processed_image = None
        except Exception as e:
            self.add_upscale_log(f"❌ Error viewing image: {str(e)}")
            
    def upscale_delete_image(self, image_path):
        """Delete an image from upscale gallery"""
        try:
            filename = os.path.basename(image_path)
            
            # Find and remove from gallery list
            for i, item in enumerate(self.upscale_original_gallery_items):
                if item.get('path') == image_path:
                    # Destroy the frame
                    if 'frame' in item:
                        item['frame'].destroy()
                    
                    # Remove from list
                    self.upscale_original_gallery_items.pop(i)
                    break
            
            # If this was the current image, clear it
            if hasattr(self, 'upscale_image_path') and self.upscale_image_path == image_path:
                self.upscale_image_path = None
                self.upscale_original_image = None
                self.upscale_original_canvas.delete("all")
                self.upscale_processed_canvas.delete("all")
                self.upscale_processed_image = None
                
            self.add_upscale_log(f"🗑️ Deleted: {filename}")
            
        except Exception as e:
            self.add_upscale_log(f"❌ Error deleting image: {str(e)}")

    def create_video_gen_ui(self, parent):
        """Create the UI for the Video Gen tab with 4-frame layout."""
        # --- Main layout frames ---
        video_gen_area = Frame(parent, bg=self.colors['bg_medium'])
        video_gen_area.pack(fill=tk.BOTH, expand=True)

        # Top row - 2 large frames (full height)
        top_row = Frame(video_gen_area, bg=self.colors['bg_medium'])
        top_row.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Left top - Image upload (full width, fixed height)
        left_panel = Frame(top_row, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1, height=530)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        left_panel.pack_propagate(False)

        # Left panel header
        left_header = Frame(left_panel, bg=self.colors['bg_light'], height=40)
        left_header.pack(fill=tk.X, padx=10, pady=(10, 5))
        left_header.pack_propagate(False)

        left_title = tk.Label(left_header, text="Original Image", 
                             font=('Arial', 12, 'bold'), 
                             bg=self.colors['bg_light'], 
                             fg=self.colors['text_white'])
        left_title.pack(side=tk.LEFT, anchor='w')

        # Upload area
        self.video_gen_upload_frame = Frame(left_panel, bg=self.colors['bg_light'])
        self.video_gen_upload_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Image display area with right-click functionality
        self.video_gen_image_frame = Frame(self.video_gen_upload_frame, bg=self.colors['bg_light'])
        self.video_gen_image_frame.pack(fill=tk.BOTH, expand=True)
        
        # Bind right-click event to the frame
        self.video_gen_image_frame.bind("<Button-3>", self.show_image_context_menu)
        
        # Add instruction text in the center
        self.video_gen_instruction_label = tk.Label(self.video_gen_image_frame, 
                                                   text="Paste or select image from folder",
                                                   font=('Arial', 12, 'italic'),
                                                   fg='gray',
                                                   bg=self.colors['bg_light'])
        self.video_gen_instruction_label.pack(expand=True)

        # Right top - Video result (full width, fixed height)
        right_panel = Frame(top_row, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1, height=530)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        right_panel.pack_propagate(False)

        # Right panel header
        right_header = Frame(right_panel, bg=self.colors['bg_light'], height=40)
        right_header.pack(fill=tk.X, padx=10, pady=(10, 5))
        right_header.pack_propagate(False)

        right_title = tk.Label(right_header, text="Generated Video", 
                              font=('Arial', 12, 'bold'), 
                              bg=self.colors['bg_light'], 
                              fg=self.colors['text_white'])
        right_title.pack(side=tk.LEFT, anchor='w')

        # Video display area
        self.video_gen_result_frame = Frame(right_panel, bg=self.colors['bg_light'])
        self.video_gen_result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Video placeholder
        self.video_gen_result_label = tk.Label(self.video_gen_result_frame, 
                                              text="Video will appear here", 
                                              font=('Arial', 12), 
                                              bg=self.colors['bg_light'], 
                                              fg=self.colors['text_gray'])
        self.video_gen_result_label.pack(fill=tk.BOTH, expand=True)

        # Bottom row - 2 small frames (increased height by 50%)
        bottom_row = Frame(video_gen_area, bg=self.colors['bg_medium'], height=225)
        bottom_row.pack(fill=tk.X, padx=20, pady=(10, 0))
        bottom_row.pack_propagate(False)

        # Left bottom - Script input
        script_frame = Frame(bottom_row, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1)
        script_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        script_header = Frame(script_frame, bg=self.colors['bg_light'], height=30)
        script_header.pack(fill=tk.X, padx=10, pady=(5, 0))
        script_header.pack_propagate(False)

        script_title = tk.Label(script_header, text="Script Prompt", 
                               font=('Arial', 10, 'bold'), 
                               bg=self.colors['bg_light'], 
                               fg=self.colors['text_white'])
        script_title.pack(side=tk.LEFT, anchor='w')
        
        # Script buttons in header
        # Generate Script button
        self.generate_script_btn = tk.Button(script_header, 
                                           text="Generate Script", 
                                           command=self.generate_script,
                                           bg=self.colors['accent'], 
                                           fg='black', 
                                           relief=tk.FLAT, 
                                           bd=0, 
                                           font=('Arial', 9, 'bold'),
                                           width=14, height=2)
        self.generate_script_btn.pack(side=tk.RIGHT, padx=(2, 0))
        
        # Clear Script button
        self.clear_script_btn = tk.Button(script_header, 
                                        text="Clear", 
                                        command=self.clear_script,
                                        bg='#f44336', 
                                        fg='black', 
                                        relief=tk.FLAT, 
                                        bd=0, 
                                        font=('Arial', 9, 'bold'),
                                        width=10, height=2)
        self.clear_script_btn.pack(side=tk.RIGHT, padx=(2, 0))
        
        # Save Script button
        self.save_script_btn = tk.Button(script_header, 
                                       text="Save", 
                                       command=self.save_script,
                                       bg='#4CAF50', 
                                       fg='black', 
                                       relief=tk.FLAT, 
                                       bd=0, 
                                       font=('Arial', 9, 'bold'),
                                       width=10, height=2)
        self.save_script_btn.pack(side=tk.RIGHT, padx=(2, 0))

        self.video_gen_script_text = tk.Text(script_frame, 
                                           height=4, 
                                           bg=self.colors['bg_dark'], 
                                           fg=self.colors['text_white'],
                                           font=('Arial', 9),
                                           wrap=tk.WORD)
        self.video_gen_script_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Right bottom - Controls
        controls_frame = Frame(bottom_row, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1)
        controls_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        controls_header = Frame(controls_frame, bg=self.colors['bg_light'], height=30)
        controls_header.pack(fill=tk.X, padx=10, pady=(5, 0))
        controls_header.pack_propagate(False)

        controls_title = tk.Label(controls_header, text="Controls", 
                                 font=('Arial', 10, 'bold'), 
                                 bg=self.colors['bg_light'], 
                                 fg=self.colors['text_white'])
        controls_title.pack(side=tk.LEFT, anchor='w')

        self.create_video_gen_controls(controls_frame)

        # Initialize video gen variables
        self.video_gen_image_path = None
        self.video_gen_original_image = None
        self.video_gen_tk_image = None
        self.video_gen_result_video = None
        self.video_gen_saved_script = None
        
        # Set default script
        default_script = """A stunning, ultra-high-quality, 8-second cinematic video. The video must be a single, seamless 'living animation' of the provided input image, with strict consistency across the model, attire, t-shirt design, and overall environment.

**Aesthetic & Mood:** Achieve a premium, film-like quality with **warm, cinematic color grading**. The scene should have a **'Hygge' or 'Cozy Lifestyle'** mood, with soft, directional lighting that creates flattering shadows and highlights.

**Consistency & Context:** Replicate the exact visual elements of the input mockup. Focus on making the **fabric texture** of the t-shirt look incredibly soft and realistic.

**Action (The Animation):** The model, starting in the pose from the input photo, performs two subtle, appealing actions simultaneously:
1.  **Head & Expression:** The model holds a **gentle, genuine smile** for the duration, slightly tilting their head, then slowly looking directly at the camera.
2.  **Prop Interaction:** They are holding a mug of coffee or tea. They **slowly raise the mug** and take a small, delicate sip, making the action feel relaxed and unhurried. The movement should allow the t-shirt to ripple very lightly.

**Camera (Dynamic Movement):** The camera should not be static. It executes a **slow, subtle 'dolly in' (tiến vào)** combined with a slight **'orbit' (xoay nhẹ)** around the model, increasing the sense of depth and dimensionality over the full 8 seconds. Use a **very shallow depth of field (bokeh)** to beautifully blur the background elements and keep the focus laser-sharp on the model and the t-shirt design.

**Style & Lighting:** **Masterpiece-level photorealism.** Golden Hour lighting style, with the suggestion of **soft lens flare** adding to the dreamy atmosphere.

**Audio:** Soft, crackling ambient sound (like a fireplace or soft coffee shop chatter), no music."""
        
        self.video_gen_script_text.insert('1.0', default_script)

    def show_image_context_menu(self, event):
        """Show context menu for image upload options."""
        context_menu = tk.Menu(self.root, tearoff=0, bg='#2c2c2c', fg='white', 
                              activebackground='#0078d4', activeforeground='white')
        
        context_menu.add_command(label="Paste Image from Clipboard", 
                               command=self.paste_image_from_clipboard)
        context_menu.add_command(label="Browse Files...", 
                               command=self.upload_video_gen_image)
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def paste_image_from_clipboard(self):
        """Paste image from clipboard."""
        try:
            from PIL import ImageGrab
            
            # Try to get image from clipboard using PIL ImageGrab (same as extract design)
            image = ImageGrab.grabclipboard()
            
            if image is not None:
                # Successfully got image from clipboard
                self.video_gen_original_image = image
                self.video_gen_image_path = "clipboard_image.png"  # Dummy path for compatibility
                self._display_uploaded_image()
                self.add_video_gen_log("📋 Image pasted from clipboard successfully!")
                return
            
            # If no image, try to get file path from clipboard
            try:
                clipboard_data = self.root.clipboard_get()
                if os.path.exists(clipboard_data):
                    if clipboard_data.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                        # Load image from file path
                        self.video_gen_image_path = clipboard_data
                        self.video_gen_original_image = Image.open(clipboard_data)
                        self._display_uploaded_image()
                        self.add_video_gen_log(f"📋 Pasted image from clipboard: {os.path.basename(clipboard_data)}")
                        return
            except:
                pass
            
            # If all methods fail, show warning
            tk.messagebox.showwarning("Warning", "No valid image found in clipboard.\n\nPlease copy an image to clipboard first, then try again.")
            
        except Exception as e:
            print(f"Error pasting from clipboard: {e}")
            tk.messagebox.showerror("Error", f"Failed to paste image from clipboard: {str(e)}")

    def _display_uploaded_image(self):
        """Display the uploaded image in the frame."""
        if self.video_gen_original_image:
            # Hide instruction text safely
            if hasattr(self, 'video_gen_instruction_label') and self.video_gen_instruction_label.winfo_exists():
                self.video_gen_instruction_label.pack_forget()
            
            # Clear previous image widgets
            for widget in self.video_gen_image_frame.winfo_children():
                if widget != self.video_gen_instruction_label:
                    widget.destroy()
            
            # Force frame to update and get proper dimensions
            self.video_gen_image_frame.update_idletasks()
            
            # Get frame dimensions
            frame_width = self.video_gen_image_frame.winfo_width()
            frame_height = self.video_gen_image_frame.winfo_height()
            
            # Calculate resize to fill the frame (may crop if aspect ratio differs)
            if frame_width > 0 and frame_height > 0:
                # Calculate scale factor to fill the frame
                img_width, img_height = self.video_gen_original_image.size
                scale_x = frame_width / img_width
                scale_y = frame_height / img_height
                scale_factor = max(scale_x, scale_y)  # Use max to fill completely
                
                new_width = int(img_width * scale_factor)
                new_height = int(img_height * scale_factor)
                
                # Resize image
                display_image = self.video_gen_original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Crop to frame size if needed
                if new_width > frame_width or new_height > frame_height:
                    left = (new_width - frame_width) // 2
                    top = (new_height - frame_height) // 2
                    right = left + frame_width
                    bottom = top + frame_height
                    display_image = display_image.crop((left, top, right, bottom))
            else:
                # Fallback if frame dimensions not available
                display_image = self.video_gen_original_image.copy()
                display_image.thumbnail((400, 400), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            self.video_gen_tk_image = ImageTk.PhotoImage(display_image)
            
            # Create label to display image (fill entire frame)
            image_label = tk.Label(self.video_gen_image_frame, 
                                image=self.video_gen_tk_image, 
                                bg=self.colors['bg_light'])
            image_label.pack(fill=tk.BOTH, expand=True)

    def create_video_gen_controls(self, parent):
        """Create controls for video generation."""
        controls_content = Frame(parent, bg=self.colors['bg_light'])
        controls_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Generate button
        self.video_gen_btn = tk.Button(controls_content, 
                                     text="🎬 Generate Video", 
                                     command=self.generate_video,
                                     bg=self.colors['accent'], 
                                     fg='black', 
                                     relief=tk.FLAT, 
                                     bd=0, 
                                     font=('Arial', 10, 'bold'),
                                     height=2)
        self.video_gen_btn.pack(fill=tk.X, pady=(0, 10))

        # Progress bar
        self.video_gen_progressbar = ttk.Progressbar(controls_content, mode='indeterminate')
        self.video_gen_progressbar.pack(fill=tk.X, pady=(0, 10))

        # Save button
        self.video_gen_save_btn = tk.Button(controls_content, 
                                          text="💾 Save Video", 
                                          command=self.save_generated_video,
                                          bg='#4CAF50', 
                                          fg='black', 
                                          relief=tk.FLAT, 
                                          bd=0, 
                                          font=('Arial', 10, 'bold'),
                                          state='disabled')
        self.video_gen_save_btn.pack(fill=tk.X, pady=(0, 10))

        # Clear button
        self.video_gen_clear_btn = tk.Button(controls_content, 
                                          text="🗑️ Clear", 
                                          command=self.clear_video_gen_widgets,
                                          bg='#f44336', 
                                          fg='black', 
                                          relief=tk.FLAT, 
                                          bd=0, 
                                          font=('Arial', 10, 'bold'))
        self.video_gen_clear_btn.pack(fill=tk.X)

    def add_video_gen_log(self, message):
        """Add message to video generation log (simplified)."""
        # Simple print to console instead of UI log
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        print(f"{timestamp} {message}")

    def clear_video_gen_widgets(self):
        """Clear all widgets and data in the video gen tab."""
        self.video_gen_image_path = None
        self.video_gen_original_image = None
        self.video_gen_tk_image = None
        self.video_gen_result_video = None
        self.video_gen_saved_script = None

        # Clear image display
        for widget in self.video_gen_image_frame.winfo_children():
            widget.destroy()

        # Show instruction text again
        if hasattr(self, 'video_gen_instruction_label') and self.video_gen_instruction_label.winfo_exists():
            self.video_gen_instruction_label.pack(expand=True)

        # Clear video display
        if hasattr(self, 'video_gen_result_label') and self.video_gen_result_label.winfo_exists():
            self.video_gen_result_label.config(text="Video will appear here")

        # Disable save button
        self.video_gen_save_btn.config(state='disabled')

        # Clear log (simplified)
        self.add_video_gen_log("Cleared. Ready for new image.")

    def generate_script(self):
        """Generate script using Gemini API."""
        try:
            # Get API key
            api_key = self.gemini_api_key_var.get().strip()
            if not api_key:
                messagebox.showwarning("Warning", "Please set your Gemini API key first.")
                return
            
            # Disable button during generation
            self.generate_script_btn.config(state='disabled', text="⏳ Generating...")
            
            # Start generation in separate thread
            import threading
            thread = threading.Thread(target=self._generate_script_thread, args=(api_key,))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.add_video_gen_log(f"Error starting script generation: {str(e)}")
            messagebox.showerror("Error", f"Failed to start script generation: {str(e)}")

    def _generate_script_thread(self, api_key):
        """Generate script in separate thread."""
        try:
            self.add_video_gen_log("🎬 Generating script with Gemini...")
            
            # Create Gemini client
            from gemini_client import GeminiClient
            client = GeminiClient(api_key=api_key)
            
            # Generate 2 different scripts for 2 videos
            self.add_video_gen_log("🎬 Generating script for Video 1 (Close-up)...")
            prompt1 = "Viết kịch bản đơn giản cho video TikTok 8s - GÓC QUAY CLOSE-UP:\n- Camera gần, tập trung vào thiết kế áo\n- Zoom in để thấy rõ chi tiết, màu sắc\n- Tỉ lệ 9:16 FULL FRAME\n- KHÔNG có text, subtitle hay chữ viết gì\n- Chỉ video thuần, không overlay"
            
            script1 = client.generate_text(prompt1)
            if not script1:
                raise Exception("Failed to generate script 1")
            
            self.add_video_gen_log("✅ Script 1 generated!")
            self.add_video_gen_log("🎬 Generating script for Video 2 (Full body)...")
            
            prompt2 = "Viết kịch bản đơn giản cho video TikTok 8s - GÓC QUAY TOÀN THÂN:\n- Camera xa, thấy cả người mặc áo\n- Người xoay người, giơ tay để show áo\n- Tỉ lệ 9:16 FULL FRAME\n- KHÔNG có text, subtitle hay chữ viết gì\n- Chỉ video thuần, không overlay"
            
            script2 = client.generate_text(prompt2)
            if not script2:
                raise Exception("Failed to generate script 2")
            
            self.add_video_gen_log("✅ Script 2 generated!")
            
            # Combine both scripts
            script = f"🎬 VIDEO 1 (8s) - CLOSE-UP FOCUS:\n{script1}\n\n" + \
                    f"🎬 VIDEO 2 (8s) - FULL BODY MOVEMENT:\n{script2}\n\n" + \
                    f"📝 FINAL: Ghép 2 video trên thành 1 video 16s hoàn chỉnh"
            
            if script:
                # Update UI in main thread
                self.root.after(0, self._display_generated_script, script)
            else:
                self.root.after(0, self._finish_script_generation, False)
                
        except Exception as e:
            self.add_video_gen_log(f"❌ Script generation failed: {str(e)}")
            self.root.after(0, self._finish_script_generation, False)

    def _display_generated_script(self, script):
        """Display the generated script in the text widget."""
        try:
            # Clear existing content
            self.video_gen_script_text.delete('1.0', tk.END)
            
            # Insert generated script
            self.video_gen_script_text.insert('1.0', script)
            
            self.add_video_gen_log("✅ Script generated successfully!")
            self._finish_script_generation(True)
            
        except Exception as e:
            self.add_video_gen_log(f"❌ Error displaying script: {str(e)}")
            self._finish_script_generation(False)

    def _finish_script_generation(self, success):
        """Finish script generation process."""
        # Re-enable button
        self.generate_script_btn.config(state='normal', text="✨ Generate Script")
        
        if not success:
            messagebox.showerror("Error", "Failed to generate script. Please try again.")

    def save_script(self):
        """Save script for video generation."""
        try:
            script_content = self.video_gen_script_text.get('1.0', tk.END).strip()
            
            if not script_content:
                messagebox.showwarning("Warning", "No script content to save.")
                return
            
            # Store script for video generation
            self.video_gen_saved_script = script_content
            
            self.add_video_gen_log("💾 Script saved for video generation")
            messagebox.showinfo("Success", "Script saved successfully!\nReady to generate video.")
                
        except Exception as e:
            self.add_video_gen_log(f"❌ Error saving script: {str(e)}")
            messagebox.showerror("Error", f"Failed to save script: {str(e)}")

    def clear_script(self):
        """Clear script content."""
        try:
            # Clear text widget completely
            self.video_gen_script_text.delete('1.0', tk.END)
            
            self.add_video_gen_log("🗑️ Script cleared")
            
        except Exception as e:
            self.add_video_gen_log(f"❌ Error clearing script: {str(e)}")
            messagebox.showerror("Error", f"Failed to clear script: {str(e)}")

    def upload_video_gen_image(self):
        """Handle image upload for video generation."""
        file_types = [
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Select Design Image",
            filetypes=file_types
        )
        
        if file_path:
            try:
                # Load and display the image
                self.video_gen_image_path = file_path
                self.video_gen_original_image = Image.open(file_path)
                
                # Display the image using the new method
                self._display_uploaded_image()
                
                self.add_video_gen_log(f"Image uploaded: {os.path.basename(file_path)}")
                self.add_video_gen_log("Ready to generate video. Click 'Generate Video' button.")
                
            except Exception as e:
                self.add_video_gen_log(f"Error loading image: {str(e)}")
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def generate_video(self):
        """Generate video using Gemini Veo3 API."""
        if not self.video_gen_image_path:
            messagebox.showwarning("Warning", "Please upload a design image first.")
            return
        
        if not self.video_gen_saved_script:
            messagebox.showwarning("Warning", "Please save a script first using the 'Save' button.")
            return
        
        # Start progress bar
        self.video_gen_progressbar.start()
        self.video_gen_btn.config(state='disabled')
        
        # Run video generation in a separate thread
        threading.Thread(target=self._generate_video_thread, daemon=True).start()

    def _generate_video_thread(self):
        """Thread function for video generation."""
        try:
            self.add_video_gen_log("Starting video generation...")
            
            # Import Gemini client
            from gemini_client import GeminiClient
            
            # Get API key
            api_key = self.gemini_api_key_var.get().strip()
            if not api_key:
                self.add_video_gen_log("Error: Gemini API key is required")
                self.root.after(0, lambda: messagebox.showerror("Error", "Gemini API key is required"))
                return
            
            # Initialize Gemini client
            gemini_client = GeminiClient(api_key)
            
            # Use saved script
            prompt = self.video_gen_saved_script
            if not prompt:
                self.add_video_gen_log("Error: Saved script is required")
                self.root.after(0, lambda: messagebox.showerror("Error", "Saved script is required"))
                return
            
            self.add_video_gen_log("Sending request to Gemini Veo3 API...")
            self.add_video_gen_log("🎬 Creating 2 videos with different camera angles...")
            
            # Generate dual videos (2x 8s videos merged into 16s)
            video_path = gemini_client.generate_dual_videos_from_image(
                image_path=self.video_gen_image_path,
                combined_script=prompt
            )
            
            if video_path and os.path.exists(video_path):
                self.video_gen_result_video = video_path
                self.add_video_gen_log("Video generated successfully!")
                self.add_video_gen_log(f"Video saved to: {os.path.basename(video_path)}")
                
                # Record usage for billing
                self.record_video_usage()
                
                # Update UI in main thread
                self.root.after(0, self._display_generated_video)
            else:
                self.add_video_gen_log("Error: Video generation failed")
                self.root.after(0, lambda: messagebox.showerror("Error", "Video generation failed"))
                
        except Exception as e:
            self.add_video_gen_log(f"Error during video generation: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Video generation failed: {str(e)}"))
        
        finally:
            # Stop progress bar and re-enable button
            self.root.after(0, self._finish_video_generation)

    def _display_generated_video(self):
        """Display the generated video in the UI."""
        if self.video_gen_result_video:
            # Clear previous content
            for widget in self.video_gen_result_frame.winfo_children():
                widget.destroy()
            
            # Create video preview frame
            video_preview_frame = Frame(self.video_gen_result_frame, bg=self.colors['bg_light'])
            video_preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Create video player using OpenCV
            try:
                import cv2
                
                # Create a frame for video display
                video_display_frame = Frame(video_preview_frame, bg=self.colors['bg_dark'], height=300)
                video_display_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
                video_display_frame.pack_propagate(False)
                
                # Create video canvas for displaying frames
                self.video_canvas = tk.Canvas(video_display_frame, 
                                            bg=self.colors['bg_dark'], 
                                            height=280,
                                            width=200)  # 9:16 aspect ratio
                self.video_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                # Force canvas to update and get proper dimensions
                self.video_canvas.update_idletasks()
                
                # Initialize video playback variables
                self.video_cap = None
                self.is_playing = False
                self.is_paused = False
                self.video_thread = None
                
                # Start video playback automatically after a short delay
                self.root.after(500, self.start_video_playback)
                
            except Exception as e:
                # Fallback to simple text display
                video_name = os.path.basename(self.video_gen_result_video)
                video_placeholder = tk.Label(video_preview_frame, 
                                           text=f"🎬 Video Generated Successfully!\n\nFile: {video_name}\n\nClick 'Save Video' to download",
                                           font=('Arial', 12),
                                           fg=self.colors['accent'],
                                           bg=self.colors['bg_light'],
                                           justify=tk.CENTER)
                video_placeholder.pack(fill=tk.BOTH, expand=True)

    def _finish_video_generation(self):
        """Finish video generation process."""
        self.video_gen_progressbar.stop()
        self.video_gen_btn.config(state='normal')
        # Enable save button if video was generated
        if self.video_gen_result_video:
            self.video_gen_save_btn.config(state='normal')

    def save_generated_video(self):
        """Save the generated video to user's chosen location."""
        if not self.video_gen_result_video:
            messagebox.showwarning("Warning", "No video to save.")
            return
        
        # Ask user for save location
        file_path = filedialog.asksaveasfilename(
            title="Save Generated Video",
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                import shutil
                shutil.copy2(self.video_gen_result_video, file_path)
                self.add_video_gen_log(f"Video saved to: {file_path}")
                messagebox.showinfo("Success", f"Video saved successfully to:\n{file_path}")
            except Exception as e:
                self.add_video_gen_log(f"Error saving video: {str(e)}")
                messagebox.showerror("Error", f"Failed to save video: {str(e)}")

    # open_video_folder function removed for cleaner interface

    def start_video_playback(self):
        """Start video playback using OpenCV."""
        if not self.video_gen_result_video:
            return
        
        try:
            import cv2
            
            # Open video file
            self.video_cap = cv2.VideoCapture(self.video_gen_result_video)
            
            if not self.video_cap.isOpened():
                self.add_video_gen_log("Error: Could not open video file")
                return
            
            # Get video properties
            fps = self.video_cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(self.video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps if fps > 0 else 0
            
            self.add_video_gen_log(f"Video loaded: {duration:.1f}s, {fps:.1f} FPS")
            
            # Start playback thread
            self.is_playing = True
            self.is_paused = False
            self.video_thread = threading.Thread(target=self._video_playback_loop, daemon=True)
            self.video_thread.start()
            
            # Update button text
            self.play_pause_btn.config(text="⏸️ Pause")
            
        except Exception as e:
            self.add_video_gen_log(f"Error starting video playback: {str(e)}")

    def _video_playback_loop(self):
        """Video playback loop running in separate thread."""
        try:
            import cv2
            import time
            
            frame_delay = 1.0 / 30.0  # 30 FPS display rate
            frame_count = 0
            
            self.add_video_gen_log("Video playback loop started")
            
            while self.is_playing and self.video_cap and self.video_cap.isOpened():
                if not self.is_paused:
                    ret, frame = self.video_cap.read()
                    
                    if not ret:
                        # End of video, restart
                        self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        self.add_video_gen_log("Video restarted")
                        continue
                    
                    frame_count += 1
                    
                    # Resize frame to fit canvas (9:16 aspect ratio)
                    canvas_width = self.video_canvas.winfo_width()
                    canvas_height = self.video_canvas.winfo_height()
                    
                    if canvas_width > 0 and canvas_height > 0:
                        # Calculate aspect ratio preserving resize
                        frame_height, frame_width = frame.shape[:2]
                        aspect_ratio = frame_width / frame_height
                        
                        if aspect_ratio > canvas_width / canvas_height:
                            # Frame is wider, fit to width
                            new_width = canvas_width
                            new_height = int(canvas_width / aspect_ratio)
                        else:
                            # Frame is taller, fit to height
                            new_height = canvas_height
                            new_width = int(canvas_height * aspect_ratio)
                        
                        # Resize frame
                        resized_frame = cv2.resize(frame, (new_width, new_height))
                        
                        # Convert BGR to RGB
                        rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                        
                        # Convert to PIL Image
                        pil_image = Image.fromarray(rgb_frame)
                        
                        # Convert to PhotoImage
                        photo = ImageTk.PhotoImage(pil_image)
                        
                        # Update canvas in main thread
                        self.root.after(0, self._update_video_frame, photo)
                        
                        # Log first few frames for debugging
                        if frame_count <= 3:
                            self.add_video_gen_log(f"Frame {frame_count}: {new_width}x{new_height}")
                    else:
                        if frame_count <= 3:
                            self.add_video_gen_log(f"Canvas size invalid: {canvas_width}x{canvas_height}")
                
                time.sleep(frame_delay)
                
        except Exception as e:
            self.add_video_gen_log(f"Error in video playback loop: {str(e)}")
            import traceback
            self.add_video_gen_log(f"Traceback: {traceback.format_exc()}")

    def _update_video_frame(self, photo):
        """Update video frame on canvas (called from main thread)."""
        try:
            if hasattr(self, 'video_canvas') and self.video_canvas.winfo_exists():
                # Clear canvas and display new frame
                self.video_canvas.delete("all")
                canvas_width = self.video_canvas.winfo_width()
                canvas_height = self.video_canvas.winfo_height()
                
                self.video_canvas.create_image(
                    canvas_width // 2,
                    canvas_height // 2,
                    image=photo,
                    anchor=tk.CENTER
                )
                # Keep reference to prevent garbage collection
                self.video_canvas.image = photo
            else:
                self.add_video_gen_log("Canvas not available for frame update")
        except Exception as e:
            self.add_video_gen_log(f"Error updating video frame: {str(e)}")

    def toggle_video_playback(self):
        """Toggle video playback between play and pause."""
        try:
            if self.is_paused:
                self.is_paused = False
                self.play_pause_btn.config(text="⏸️ Pause")
                self.add_video_gen_log("Video resumed")
            else:
                self.is_paused = True
                self.play_pause_btn.config(text="▶️ Play")
                self.add_video_gen_log("Video paused")
        except Exception as e:
            self.add_video_gen_log(f"Error toggling video playback: {str(e)}")

    def stop_video_playback(self):
        """Stop video playback."""
        try:
            self.is_playing = False
            self.is_paused = False
            
            if self.video_cap:
                self.video_cap.release()
                self.video_cap = None
            
            # Clear canvas
            if hasattr(self, 'video_canvas'):
                self.video_canvas.delete("all")
                self.video_canvas.create_text(
                    self.video_canvas.winfo_width() // 2,
                    self.video_canvas.winfo_height() // 2,
                    text="Video Stopped",
                    fill=self.colors['text_gray'],
                    font=('Arial', 14)
                )
            
            self.play_pause_btn.config(text="▶️ Play")
            self.add_video_gen_log("Video stopped")
            
        except Exception as e:
            self.add_video_gen_log(f"Error stopping video playback: {str(e)}")

    def add_upscale_log(self, message):
        """Adds a message to the upscale log (console only since we removed the log widget)."""
        timestamp = time.strftime('%H:%M:%S')
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)

    def _on_gallery_item_click(self, item_data, is_processed):
        """Handles clicks on gallery items to display them and highlight selection."""
        # --- Highlight Logic ---
        # Reset previous selection
        if self.upscale_active_item_frame:
            self.upscale_active_item_frame.configure(bg=self.colors['bg_dark'])
            for widget in self.upscale_active_item_frame.winfo_children():
                widget.configure(bg=self.colors['bg_dark'])
                if isinstance(widget, Frame): # For info_frame
                    for sub_widget in widget.winfo_children():
                        sub_widget.configure(bg=self.colors['bg_dark'])

        # Highlight new selection
        new_frame = item_data['frame']
        new_frame.configure(bg=self.colors['accent'])
        for widget in new_frame.winfo_children():
            # Don't change checkbox bg, but change its container
            if not isinstance(widget, tk.Checkbutton):
                 widget.configure(bg=self.colors['accent'])
            if isinstance(widget, Frame):
                for sub_widget in widget.winfo_children():
                    sub_widget.configure(bg=self.colors['accent'])
        self.upscale_active_item_frame = new_frame

        # --- Display Logic ---
        if is_processed:
            # Display the processed image on the right
            self._display_image_in_widget(item_data['image_data'], self.upscale_processed_canvas, "processed")
            
            # Display the corresponding original image on the left for context
            try:
                original_image = cv2.imread(item_data['path'], cv2.IMREAD_UNCHANGED)
                if original_image is not None:
                    self._display_image_in_widget(original_image, self.upscale_original_canvas, "original")
                else:
                    self.upscale_original_canvas.delete("all")
            except Exception as e:
                self.add_upscale_log(f"Error previewing original: {e}")
        else:
            # It's an original image. Set it as the active one for processing.
            try:
                original_image = cv2.imread(item_data['path'], cv2.IMREAD_UNCHANGED)
                if original_image is None: raise ValueError("Could not read image file.")
                
                self.upscale_image_path = item_data['path']
                self.upscale_original_image = original_image
                self._display_image_in_widget(original_image, self.upscale_original_canvas, "original")
                
                # Clear the processed view since it's for a different source now
                self.upscale_processed_canvas.delete("all")
                self.upscale_processed_image = None
                self.upscale_tk_processed = None

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image for preview: {e}")

    def _add_to_upscale_gallery(self, gallery_list, image_path, image_data=None, is_processed=False):
        """Helper to add a new file item to the upscale gallery."""
        filename = os.path.basename(image_path)
        
        if is_processed:
            # Add to processed results container
            item_frame = Frame(self.upscale_processed_list_container, bg=self.colors['bg_dark'])
            item_frame.pack(pady=2, padx=5, fill=tk.X)
            
            # Checkbox for selection
            var = tk.BooleanVar(value=False)
            chk = tk.Checkbutton(item_frame, text="", variable=var, 
                               bg=self.colors['bg_dark'], selectcolor=self.colors['bg_dark'], 
                               activebackground=self.colors['bg_dark'], relief=tk.FLAT)
            chk.pack(side=tk.LEFT, padx=(5, 10))
            
            # Icon and filename
            icon_label = tk.Label(item_frame, text="✨", bg=self.colors['bg_dark'], 
                                fg=self.colors['text_white'], font=('Arial', 10))
            icon_label.pack(side=tk.LEFT, padx=(5, 2))
            
            filename_label = tk.Label(item_frame, text=filename, bg=self.colors['bg_dark'], 
                                    fg=self.colors['text_white'], anchor='w', wraplength=400, justify=tk.LEFT)
            filename_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
            
            item_data = {
                "frame": item_frame, 
                "path": image_path, 
                "image_data": image_data,
                "checkbox_var": var,
                "icon_label": icon_label
            }
            
            # Click handler for preview
            handler = lambda e, data=item_data: self._on_gallery_item_click(data, True)
            for widget in [item_frame, filename_label, icon_label]:
                widget.bind("<Button-1>", handler)
                
        else:
            # Add to original images scrollable frame
            item_frame = Frame(self.upscale_scrollable_frame, bg=self.colors['bg_dark'])
            item_frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Image icon and filename
            status_icon = "🖼️"  # Image icon for original
            label_text = f"{status_icon} {filename}"
            
            label = tk.Label(item_frame, text=label_text,
                           bg=self.colors['bg_dark'],
                           fg=self.colors['text_white'],
                           font=('Arial', 9),
                           anchor='w')
            label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
            
            # Click to view image
            label.bind("<Button-1>", lambda e, path=image_path: self.upscale_on_item_click(path))
            
            # Delete button (X icon)
            delete_btn = tk.Label(item_frame, text="×", 
                                 bg=self.colors['bg_dark'], fg='#ff4444',
                                 font=('Arial', 12, 'bold'),
                                 cursor="hand2")
            delete_btn.pack(side=tk.RIGHT, padx=(0, 5))
            delete_btn.bind("<Button-1>", lambda e, path=image_path: self.upscale_delete_image(path))
            
            item_data = {"path": image_path, "filename": filename, "frame": item_frame, "label": label}
        
        gallery_list.append(item_data)

    def toggle_upscale_checkboxes(self, state):
        """Toggles all checkboxes in the processed results gallery."""
        for item in self.upscale_processed_gallery_items:
            if "checkbox_var" in item:
                item["checkbox_var"].set(state)

    def _toggle_original_image_checkboxes(self):
        """Shows or hides the checkboxes in the original images gallery based on batch mode state."""
        is_batch_mode = self.upscale_batch_mode_var.get()
        for item in self.upscale_original_gallery_items:
            chk = item.get("checkbox_widget")
            filename_label = item.get("filename_label")
            if chk and filename_label:
                if is_batch_mode:
                    chk.pack(side=tk.LEFT, padx=(5, 10), before=filename_label)
                else:
                    chk.pack_forget()

    def cleanup_temporary_items_on_startup(self):
        """Cleans up temporary items when the app starts."""
        try:
            # Clear any existing temporary items
            if hasattr(self, 'redesign_processed_items'):
                self.redesign_processed_items = []
            self.add_log("Cleaned up temporary items on startup")
        except Exception as e:
            self.add_log(f"Error cleaning up temporary items on startup: {e}")

    def on_closing(self):
        """Cleanup when closing the application."""
        try:
            # Clear mockup template cache
            if hasattr(self, 'mockup_cache'):
                self.mockup_cache.clear_cache()
                self.add_log("📦 Mockup template cache cleared on exit")
        except Exception as e:
            self.add_log(f"Error during cleanup: {e}")
        
        # Destroy the root window
        self.root.destroy()

    def save_selected_upscaled(self):
        """Saves all selected images from the processed gallery to a chosen directory."""
        selected_items = [item for item in self.upscale_processed_gallery_items if item.get("checkbox_var") and item["checkbox_var"].get()]
        
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select at least one image to save.")
            return

        output_dir = filedialog.askdirectory(title="Select Folder to Save Images")
        if not output_dir: return

        count = 0
        for item in selected_items:
            try:
                original_name = os.path.splitext(os.path.basename(item['path']))[0]
                model_name = self.upscale_model_var.get()
                save_name = f"{original_name}_{model_name}_{count}.png" # Add count to avoid overwrite
                save_path = os.path.join(output_dir, save_name)
                
                cv2.imwrite(save_path, item['image_data'])
                self.add_upscale_log(f"Saved: {save_name}")
                count += 1
            except Exception as e:
                self.add_upscale_log(f"Error saving {item['path']}: {e}")
        
        if count > 0:
            messagebox.showinfo("Save Complete", f"Successfully saved {count} image(s) to:\n{output_dir}")

    def browse_upscale_image(self):
        """Opens a dialog to select an image for upscaling."""
        paths = filedialog.askopenfilenames(
            title="Select an Image",
            filetypes=(("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*"))
        )
        if not paths:
            return

        # Clear previous processed data
        self.upscale_processed_canvas.delete("all")
        self.upscale_processed_image = None
        
        # Use the helper function to add images
        self.upscale_add_image_files(paths)

    def process_upscale_image(self):
        """Starts the upscale process and changes the button to 'Cancel'."""
        self.upscale_cancel_event.clear()
        self.process_upscale_btn.config(text="Cancel", command=self.cancel_upscale_process)

        if self.upscale_batch_mode_var.get():
            items_to_process = [item for item in self.upscale_original_gallery_items if item.get("checkbox_var") and item["checkbox_var"].get()]
            if not items_to_process:
                messagebox.showwarning("Warning", "Please select images for batch mode.")
                self._reset_upscale_ui()
                return
            threading.Thread(target=self._process_upscale_batch_thread, args=(items_to_process,), daemon=True).start()
        else:
            if self.upscale_original_image is None:
                messagebox.showwarning("Warning", "Please select an image to process.")
                self._reset_upscale_ui()
                return
            
            model = self.upscale_model_var.get()
            scale_factor = 4
            
            threading.Thread(target=self._process_upscale_thread, args=(
                self.upscale_original_image, 
                self.upscale_image_path, 
                model, 
                scale_factor
            ), daemon=True).start()

    def cancel_upscale_process(self):
        """Sets the event to signal cancellation to the running thread."""
        self.add_upscale_log("Cancellation requested...")
        self.upscale_cancel_event.set()
        self.process_upscale_btn.config(state='disabled')

    def _reset_upscale_ui(self):
        """Resets the UI elements to their initial state after processing or cancellation."""
        self.process_upscale_btn.config(text="Process", command=self.process_upscale_image, state='normal')
        self.upscale_progressbar.config(mode='indeterminate', value=0)
        self.upscale_progressbar.stop()

    def _process_upscale_batch_thread(self, items_to_process):
        """Processes all selected images in the original gallery in a background thread."""
        original_logger = self.processor.log_callback
        try:
            self.processor.log_callback = self.add_upscale_log # Temporarily redirect logs
            model = self.upscale_model_var.get()
            scale_factor = 4
            total_items = len(items_to_process)

            self.root.after(0, self.upscale_progressbar.config, {'mode': 'determinate', 'maximum': total_items, 'value': 0})
            self.add_upscale_log(f"Starting batch upscale for {total_items} images...")

            for i, item in enumerate(items_to_process):
                if self.upscale_cancel_event.is_set():
                    self.add_upscale_log("Batch process cancelled by user.")
                    break
                try:
                    path = item['path']
                    original_image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
                    if original_image is None:
                        self.add_upscale_log(f"   -> Skipping, could not read {os.path.basename(path)}.")
                        self.root.after(0, self.upscale_progressbar.step)
                        continue
                    
                    self.add_upscale_log(f"Processing ({i + 1}/{total_items}): {os.path.basename(path)}")
                    processed_image = self.processor._run_ai_upscale(original_image, model, scale_factor)
                    
                    # Up Scale tab is FREE - no usage tracking
                    
                    self.root.after(0, self._update_ui_after_batch_item, path, processed_image)
                except Exception as e:
                    if "cancelled" not in str(e).lower():
                        self.add_upscale_log(f"   -> Error processing {os.path.basename(path)}: {e}")
                    self.root.after(0, self.upscale_progressbar.step)
            self.add_upscale_log("Batch processing finished.")
        finally:
            self.processor.log_callback = original_logger # Restore the original logger
            self.root.after(0, self._reset_upscale_ui)

    def _update_ui_after_batch_item(self, path, processed_image):
        """Callback to update UI from batch thread. Adds item to gallery and steps progress."""
        if not self.upscale_cancel_event.is_set():
            self._add_to_upscale_gallery(
                self.upscale_processed_gallery_items,
                path,
                image_data=processed_image,
                is_processed=True
            )
        self.upscale_progressbar.step()

    def _process_upscale_thread(self, original_image, image_path, model, scale_factor):
        """Processes the single selected image in a background thread."""
        original_logger = self.processor.log_callback
        try:
            self.processor.log_callback = self.add_upscale_log # Temporarily redirect logs

            self.add_upscale_log(f"Starting upscale process for {os.path.basename(image_path)}...")
            self.root.after(0, self.upscale_progressbar.start)

            self.upscale_processed_image = self.processor._run_ai_upscale(original_image, model, scale_factor)
            self.add_upscale_log("Upscale successful!")
            
            # Up Scale tab is FREE - no usage tracking
            
            self.root.after(0, self._update_upscale_ui_after_processing)

        except Exception as e:
            if "cancelled" in str(e).lower():
                self.add_upscale_log("Process cancelled.")
            else:
                self.add_upscale_log(f"Error during upscale: {e}")
                self.root.after(0, lambda e=e: messagebox.showerror("Error", f"An error occurred during upscaling:\n{e}"))
        finally:
            self.processor.log_callback = original_logger # Restore the original logger
            self.root.after(0, self._reset_upscale_ui)

    def _update_upscale_ui_after_processing(self):
        """Updates the UI after the upscale thread is complete. Must be called from the main thread."""
        if self.upscale_cancel_event.is_set():
            return
        self._display_image_in_widget(self.upscale_processed_image, self.upscale_processed_canvas, "processed")
        
        self._add_to_upscale_gallery(
            self.upscale_processed_gallery_items,
            self.upscale_image_path,
            image_data=self.upscale_processed_image,
            is_processed=True
        )

    def _display_image_in_widget(self, cv_image, widget, image_type):
        """Converts CV2 image to PhotoImage and displays it in a widget (Label or Canvas)."""
        if cv_image is None:
            return

        widget_w = widget.winfo_width()
        widget_h = widget.winfo_height()
        
        if widget_w < 2 or widget_h < 2: # Wait for widget to be drawn
             self.root.after(100, self._display_image_in_widget, cv_image, widget, image_type)
             return

        h, w = cv_image.shape[:2]
        aspect_ratio = w / h
        
        if w > widget_w or h > widget_h:
            if w/widget_w > h/widget_h:
                new_w = widget_w
                new_h = int(new_w / aspect_ratio)
            else:
                new_h = widget_h
                new_w = int(new_h * aspect_ratio)
            resized_img = cv2.resize(cv_image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        else:
            resized_img = cv_image
            
        # Convert to PhotoImage
        if len(resized_img.shape) == 3 and resized_img.shape[2] == 4:
            img_rgb = cv2.cvtColor(resized_img, cv2.COLOR_BGRA2RGBA)
        else:
            img_rgb = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
            
        pil_img = Image.fromarray(img_rgb)
        photo_img = ImageTk.PhotoImage(pil_img)
        
        # Keep a reference
        if image_type == "original":
            self.upscale_tk_original = photo_img
        else:
            self.upscale_tk_processed = photo_img

        if isinstance(widget, tk.Canvas):
            widget.delete("all")
            x_pos = (widget.winfo_width() - photo_img.width()) / 2
            y_pos = (widget.winfo_height() - photo_img.height()) / 2
            widget.create_image(x_pos, y_pos, anchor='nw', image=photo_img)
        elif isinstance(widget, tk.Label):
            widget.config(image=photo_img)
            
    def add_save_button(self):
        """Adds a save button to the upscaled image panel."""
        # Clear any existing button first
        for widget in self.upscale_save_button_frame.winfo_children():
            widget.destroy()
             
        save_btn = tk.Button(self.upscale_save_button_frame, text="Save Image...", command=self.save_upscaled_image)
        save_btn.pack()

    def save_upscaled_image(self):
        if self.upscale_processed_image is None:
            return

        original_name = os.path.splitext(os.path.basename(self.upscale_image_path))[0]
        model_name = self.upscale_model_var.get()
        
        save_path = filedialog.asksaveasfilename(
            initialfile=f"{original_name}_{model_name}_x4.png",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )

        if save_path:
            try:
                cv2.imwrite(save_path, self.upscale_processed_image)
                self.add_upscale_log(f"Image saved to: {save_path}")
                messagebox.showinfo("Success", f"Image saved successfully to:\n{save_path}")
            except Exception as e:
                self.add_upscale_log(f"Error saving image: {e}")
                messagebox.showerror("Error", f"Failed to save image: {e}")
        
    def create_main_area(self, parent):
        """Create main content area for the 'Extract Design' tab."""
        # This function now populates the given 'parent' frame
        main_area = Frame(parent, bg=self.colors['bg_medium'])
        main_area.pack(fill=tk.BOTH, expand=True)
        
        # Main content panels (expanded to fill more space)
        self.create_content_panels(main_area)
        
        # Bottom section
        self.create_bottom_section(main_area)
        
        # Footer
        self.create_footer(main_area)
        
    def create_footer(self, parent):
        """Create footer with copyright"""
        footer = Frame(parent, bg=self.colors['bg_medium'], height=25)
        footer.pack(fill=tk.X, padx=20, pady=(0, 10))
        footer.pack_propagate(False)
        
        # Copyright label
        copyright_label = tk.Label(footer, text="Copyright 2025 © JEG Technology",
                                  bg=self.colors['bg_medium'],
                                  fg=self.colors['text_gray'],
                                  font=('Arial', 9, 'italic'))
        copyright_label.pack(side=tk.LEFT, anchor='w')
        
    def create_header(self, parent):
        """Create header - now empty since we moved controls to image panels"""
        pass
        
        
        
    def create_content_panels(self, parent):
        """Create main content panels using a grid layout for equal sizing."""
        content_frame = Frame(parent, bg=self.colors['bg_medium'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 10))

        # Configure the grid to have two equally sized columns
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left panel - Original Image
        left_panel = Frame(content_frame, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        tk.Label(left_panel, text="Original Image (Select Region)",
                bg=self.colors['bg_light'], fg=self.colors['text_white'],
                font=('Arial', 12, 'bold'), pady=5).pack(fill=tk.X)
        
        self.original_canvas = Canvas(left_panel, bg='black')
        self.original_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left-click: Rectangle selection for design area
        self.original_canvas.bind("<Button-1>", self.start_selection)
        self.original_canvas.bind("<B1-Motion>", self.update_selection)
        self.original_canvas.bind("<ButtonRelease-1>", self.end_selection)
        self.original_canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Right-click: Context menu for paste
        self.original_canvas.bind("<Button-3>", self.on_right_click)
        
        # Visual feedback
        self.original_canvas.configure(cursor="crosshair")
        
        # Right panel - Extracted Design
        right_panel = Frame(content_frame, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        right_header = Frame(right_panel, bg=self.colors['bg_light'])
        right_header.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(right_header, text="Extracted Design",
                bg=self.colors['bg_light'], fg=self.colors['text_white'],
                font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        # Canvas for extracted design - will be managed by progress UI
        self.extracted_canvas = Canvas(right_panel, bg='white')
        self._create_transparent_background()
        
        # Add right-click functionality for extracted design
        self.extracted_canvas.bind("<Button-3>", self.on_right_click_extracted)  # Right click press
        self.extracted_canvas.bind("<B3-Motion>", self.on_right_drag_extracted)  # Right click drag
        self.extracted_canvas.bind("<ButtonRelease-3>", self.on_right_release_extracted)  # Right click release
        
        # Variables for tracking right-click behavior
        self.right_click_start_pos = None
        self.is_dragging = False
        self.current_zoom_image = None
        self.zoom_overlay_id = None
        
        # Progress bar and status label UI
        self.progress_frame = Frame(right_panel, bg=self.colors['bg_light'])
        # The GIF label will be created dynamically in start_gif_animation
        
        self.progress_label = tk.Label(self.progress_frame, text="Processing...",
                                      bg=self.colors['bg_light'], fg=self.colors['text_white'],
                                      font=('Arial', 10, 'italic'))
        self.progress_label.pack(pady=(10, 5))
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient='horizontal',
                                            length=200, mode='determinate')
        self.progress_bar.pack(pady=5, padx=20, fill=tk.X)
        
        self.extracted_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        # Progress frame is packed/unpacked by show_progress_ui
        self.extracted_canvas.bind("<Configure>", self.on_canvas_configure)
        
    def _create_transparent_background(self):
        """Tạo pattern checkerboard để hiển thị background trong suốt"""
        def draw_checkerboard(event=None):
            self.extracted_canvas.delete("checkerboard")
            width = self.extracted_canvas.winfo_width()
            height = self.extracted_canvas.winfo_height()
            
            if width <= 1 or height <= 1:
                return
                
            # Kích thước ô vuông checkerboard
            square_size = 10
            
            # Màu sắc cho pattern
            color1 = '#f0f0f0'  # Xám nhạt
            color2 = '#e0e0e0'  # Xám đậm hơn
            
            for y in range(0, height, square_size):
                for x in range(0, width, square_size):
                    if (x // square_size + y // square_size) % 2 == 0:
                        color = color1
                    else:
                        color = color2
                    
                    self.extracted_canvas.create_rectangle(
                        x, y, x + square_size, y + square_size,
                        fill=color, outline="", tags="checkerboard"
                    )
        
        # Vẽ checkerboard ngay lập tức
        draw_checkerboard()
        
        # Bind event để vẽ lại khi canvas thay đổi kích thước
        self.extracted_canvas.bind("<Configure>", draw_checkerboard)
        
    def _draw_checkerboard_background(self):
        """Vẽ lại pattern checkerboard cho background trong suốt"""
        width = self.extracted_canvas.winfo_width()
        height = self.extracted_canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
            
        # Kích thước ô vuông checkerboard
        square_size = 10
        
        # Màu sắc cho pattern
        color1 = '#f0f0f0'  # Xám nhạt
        color2 = '#e0e0e0'  # Xám đậm hơn
        
        for y in range(0, height, square_size):
            for x in range(0, width, square_size):
                if (x // square_size + y // square_size) % 2 == 0:
                    color = color1
                else:
                    color = color2
                
                self.extracted_canvas.create_rectangle(
                    x, y, x + square_size, y + square_size,
                    fill=color, outline="", tags="checkerboard"
                )
        
    def load_gif(self):
        """Load GIF frames and make its white-like background transparent."""
        try:
            gif_path = get_base_path() / "process-management.gif"
            if not gif_path.exists():
                self.add_log("⚠️ Warning: process-management.gif not found. Animation will be disabled.")
                return

            with Image.open(gif_path) as img:
                for frame in ImageSequence.Iterator(img):
                    rgba_frame = frame.copy().convert("RGBA")
                    data = np.array(rgba_frame)
                    
                    # Threshold for "near-white" pixels.
                    # This is more robust than checking for pure white (255,255,255)
                    # and handles anti-aliasing artifacts.
                    threshold = 240
                    near_white_pixels = (data[:,:,0] > threshold) & \
                                        (data[:,:,1] > threshold) & \
                                        (data[:,:,2] > threshold)
                    
                    # Set the alpha channel of these pixels to 0 (fully transparent)
                    data[near_white_pixels, 3] = 0
                    
                    transparent_frame = Image.fromarray(data)
                    transparent_frame.thumbnail((200, 200), Image.Resampling.LANCZOS)
                    self.gif_frames.append(ImageTk.PhotoImage(transparent_frame))
                    
            self.add_log("🖼️ Loaded and processed GIF with transparent background.")
        except Exception as e:
            self.add_log(f"❌ Error loading GIF: {e}")
            self.gif_frames = []

    def update_gif_frame(self):
        """Update the GIF frame for animation."""
        if not self.is_processing or not self.gif_frames:
            return
            
        frame = self.gif_frames[self.gif_frame_index]
        self.gif_frame_index = (self.gif_frame_index + 1) % len(self.gif_frames)
        
        if self.gif_label:
            self.gif_label.configure(image=frame)
            
        self.gif_animation_job = self.root.after(50, self.update_gif_frame) # Adjust delay for speed

    def start_gif_animation(self):
        """Start the GIF animation."""
        if not self.gif_frames: return

        if self.gif_label is None:
            # Create the label for the GIF inside the progress frame
            self.gif_label = tk.Label(self.progress_frame, bg=self.colors['bg_light'])
            self.gif_label.pack(pady=20)
            
        self.gif_frame_index = 0
        if self.gif_animation_job:
            self.root.after_cancel(self.gif_animation_job)
        self.update_gif_frame()

    def stop_gif_animation(self):
        """Stop the GIF animation."""
        if self.gif_animation_job:
            self.root.after_cancel(self.gif_animation_job)
            self.gif_animation_job = None
        if self.gif_label:
            self.gif_label.pack_forget()
            self.gif_label = None

        
    def create_bottom_section(self, parent):
        """Create bottom section with dual image lists and activity log"""
        bottom_frame = Frame(parent, bg=self.colors['bg_medium'], height=300)
        bottom_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        bottom_frame.pack_propagate(False)
        
        # Left side: Original Images + Processed Results
        images_container = Frame(bottom_frame, bg=self.colors['bg_medium'])
        images_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Original Images (Left)
        original_frame = Frame(images_container, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1)
        original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Header with title and buttons
        original_header = Frame(original_frame, bg=self.colors['bg_light'])
        original_header.pack(fill=tk.X, padx=10, pady=(5, 0))
        
        tk.Label(original_header, text="Original Images",
                bg=self.colors['bg_light'], fg=self.colors['text_white'],
                font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        # Action buttons moved here
        btn_frame = Frame(original_header, bg=self.colors['bg_light'])
        btn_frame.pack(side=tk.RIGHT)
        
        tk.Button(btn_frame, text="Browse...", 
                 bg='#e0e0e0', fg='#000000',
                 relief=tk.FLAT, bd=0, padx=10, pady=3,
                 font=('Arial', 9, 'bold'),
                 highlightbackground='#cccccc',
                 command=self.browse_files).pack(side=tk.LEFT, padx=(5, 2))
        tk.Button(btn_frame, text="Clear All",
                 bg='#e0e0e0', fg='#000000',
                 relief=tk.FLAT, bd=0, padx=10, pady=3,
                 font=('Arial', 9, 'bold'),
                 highlightbackground='#cccccc',
                 command=self.clear_all).pack(side=tk.LEFT, padx=(2, 5))
        
        # Scrollable original image list
        original_scroll_frame = Frame(original_frame, bg=self.colors['bg_light'])
        original_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Container for original image list (will switch between listbox and checkbox list)
        self.list_container = Frame(original_scroll_frame, bg=self.colors['bg_dark'])
        self.list_container.pack(fill=tk.BOTH, expand=True)
        
        # Single selection listbox (default mode)
        self.image_listbox = tk.Listbox(self.list_container, 
                                       bg=self.colors['bg_dark'],
                                       fg=self.colors['text_white'],
                                       selectbackground=self.colors['accent'])
        self.image_listbox.pack(fill=tk.BOTH, expand=True)
        self.image_listbox.bind('<<ListboxSelect>>', self.on_image_select)
        
        # Batch selection frame (hidden by default)
        # Don't pack initially
        
        # Processed Results (Right)
        processed_frame = Frame(images_container, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1)
        processed_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Header with download controls
        processed_header = Frame(processed_frame, bg=self.colors['bg_light'])
        processed_header.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(processed_header, text="Processed Results",
                bg=self.colors['bg_light'], fg=self.colors['text_white'],
                font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        # Download controls
        download_controls = Frame(processed_header, bg=self.colors['bg_light'])
        download_controls.pack(side=tk.RIGHT)
        
        tk.Button(download_controls, text="All", 
                 bg='#e0e0e0', fg='#000000',
                 relief=tk.FLAT, bd=0, padx=10, pady=3,
                 font=('Arial', 9, 'bold'),
                 highlightbackground='#cccccc',
                 command=self.select_all_download).pack(side=tk.LEFT, padx=(5, 2))
        
        tk.Button(download_controls, text="None", 
                 bg='#e0e0e0', fg='#000000',
                 relief=tk.FLAT, bd=0, padx=10, pady=3,
                 font=('Arial', 9, 'bold'),
                 highlightbackground='#cccccc',
                 command=self.select_none_download).pack(side=tk.LEFT, padx=(2, 5))
        
        # Separator
        separator = Frame(download_controls, bg='#666666', width=1, height=15)
        separator.pack(side=tk.LEFT, padx=5)
        
        # Save Results button
        tk.Button(download_controls, text="Save Results",
                 bg='#90ee90', fg='#000000',
                 relief=tk.FLAT, bd=0, padx=10, pady=3,
                 font=('Arial', 9, 'bold'),
                 highlightbackground='#cccccc',
                 command=self.save_results).pack(side=tk.LEFT, padx=(5, 5))
        
        # Scrollable processed results list
        self.processed_scroll_frame = Frame(processed_frame, bg=self.colors['bg_light'])
        self.processed_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # This will be populated dynamically
        self.processed_list_container = Frame(self.processed_scroll_frame, bg=self.colors['bg_dark'])
        self.processed_list_container.pack(fill=tk.BOTH, expand=True)
        
        # Right side - Processing Options (replaces Activity Log)
        right_bottom = Frame(bottom_frame, bg=self.colors['bg_medium'])
        right_bottom.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Processing Options Panel
        options_panel = Frame(right_bottom, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1, width=400)
        options_panel.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        options_panel.pack_propagate(False)
        
        # Options content frame
        options_content = Frame(options_panel, bg=self.colors['bg_light'])
        options_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Row 1: Output Size
        size_row = Frame(options_content, bg=self.colors['bg_light'])
        size_row.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(size_row, text="Output Size:",
                bg=self.colors['bg_light'], fg=self.colors['text_white'],
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.size_var = tk.StringVar(value="4500 x 4500 px")
        size_options = [
            "4500 x 5400 px",
            "4500 x 4500 px", 
            "1500 x 1500 px",
            "3000 x 3000 px",
            "3300 x 5100 px"
        ]
        
        self.size_dropdown = ttk.Combobox(size_row, textvariable=self.size_var,
                                         values=size_options, state="readonly", width=15,
                                         font=('Arial', 10))
        self.size_dropdown.pack(side=tk.RIGHT)
        self.size_dropdown.bind('<<ComboboxSelected>>', self.on_size_changed)
        
        
        # Fixed AI model (no dropdown needed)
        self.upscayl_model_var = tk.StringVar(value="digital-art-4x")
        
        # Processing mode variables (API mode only)
        self.processing_type_var = tk.StringVar(value="print")  # print or embroidery
        self.gemini_api_key_var = tk.StringVar(value="AIzaSyCxLhTOD-sMtaIYdw9CTKc4QVo1PHnDFpg")
        
        

        # Row 3: Processing Type
        processing_type_row = Frame(options_content, bg=self.colors['bg_light'])
        processing_type_row.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(processing_type_row, text="Type:",
                bg=self.colors['bg_light'], fg=self.colors['text_white'], 
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        # Processing type dropdown
        processing_types = ["Print", "Embroidery"]
        self.processing_type_dropdown = ttk.Combobox(processing_type_row, textvariable=self.processing_type_var,
                                                    values=processing_types, state="readonly", width=15,
                                                    font=('Arial', 10))
        self.processing_type_dropdown.pack(side=tk.RIGHT)
        self.processing_type_dropdown.bind('<<ComboboxSelected>>', self.on_processing_type_changed)
        
        # Row 4: Mockup Options
        mockup_row = Frame(options_content, bg=self.colors['bg_light'])
        mockup_row.pack(fill=tk.X, pady=(0, 10))
        
        # Mockup checkbox
        self.mockup_var = tk.BooleanVar(value=False)
        mockup_checkbox = tk.Checkbutton(mockup_row, text="Mockup",
                                       variable=self.mockup_var,
                                       bg=self.colors['bg_light'], fg=self.colors['text_white'],
                                       selectcolor=self.colors['bg_dark'],
                                       font=('Arial', 10),
                                       command=self.on_mockup_changed)
        mockup_checkbox.pack(side=tk.LEFT, padx=(0, 20))
        
        # Model checkbox (only visible when mockup is enabled)
        self.model_var = tk.BooleanVar(value=False)
        self.model_checkbox = tk.Checkbutton(mockup_row, text="Model",
                                           variable=self.model_var,
                                           bg=self.colors['bg_light'], fg=self.colors['text_white'],
                                           selectcolor=self.colors['bg_dark'],
                                           font=('Arial', 10),
                                           command=self.on_model_changed)
        self.model_checkbox.pack(side=tk.LEFT, padx=(0, 20))
        self.model_checkbox.pack_forget()  # Initially hidden
        self.mockup_type_var = tk.StringVar(value="T-shirt")
        mockup_types = ["T-shirt", "Hooded", "Sweatshirt", "Baby Rib Bodysuit", "Hat", "Mug"]
        self.mockup_type_dropdown = ttk.Combobox(mockup_row, textvariable=self.mockup_type_var,
                                                values=mockup_types, state="readonly", width=15,
                                                font=('Arial', 10))
        self.mockup_type_dropdown.pack(side=tk.RIGHT)
        self.mockup_type_dropdown.bind('<<ComboboxSelected>>', self.on_mockup_type_changed)
        
        # Row 5: Redesign Options
        redesign_row = Frame(options_content, bg=self.colors['bg_light'])
        redesign_row.pack(fill=tk.X, pady=(0, 10))
        
        # Redesign checkbox
        self.redesign_var = tk.BooleanVar(value=False)
        redesign_checkbox = tk.Checkbutton(redesign_row, text="Redesign",
                                          variable=self.redesign_var,
                                          bg=self.colors['bg_light'], fg=self.colors['text_white'],
                                                 selectcolor=self.colors['bg_dark'],
                                                 font=('Arial', 10),
                                          command=self.on_redesign_changed)
        redesign_checkbox.pack(side=tk.LEFT)
        
        # Redesign prompt form (initially hidden)
        self.redesign_form_frame = Frame(options_content, bg=self.colors['bg_light'])
        # Don't pack initially - will be shown when redesign is checked
        
        
        self.redesign_prompt_text = tk.Text(self.redesign_form_frame, height=3, width=40,
                                          bg=self.colors['bg_dark'], fg=self.colors['text_white'],
                                          font=('Arial', 9),
                                          wrap=tk.WORD)
        self.redesign_prompt_text.pack(fill=tk.X, pady=(0, 5))
        
        # Add placeholder functionality
        self.redesign_prompt_placeholder = "Write your prompt to customize design"
        self.redesign_prompt_text.insert('1.0', self.redesign_prompt_placeholder)
        self.redesign_prompt_text.configure(fg='#666666')  # Gray color for placeholder
        
        # Bind events for placeholder functionality
        self.redesign_prompt_text.bind('<FocusIn>', self.on_redesign_prompt_focus_in)
        self.redesign_prompt_text.bind('<FocusOut>', self.on_redesign_prompt_focus_out)
        self.redesign_prompt_text.bind('<KeyPress>', self.on_redesign_prompt_key)
        
        # Processing
        processing_frame = Frame(right_bottom, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1, height=60)
        processing_frame.pack(fill=tk.X)
        processing_frame.pack_propagate(False)
        
        
        # Extract button
        self.extract_btn = tk.Button(processing_frame, text="Extract Design",
                                    bg='#90ee90', fg='#000000',
                                    font=('Arial', 11, 'bold'),
                                    relief=tk.FLAT, bd=0,
                                    pady=10, command=self.extract_current_design)
        self.extract_btn.pack(fill=tk.X, padx=20, pady=15)
        
    def add_log(self, message, target_log="extract"):
        """Add message to a specific activity log."""
        # For extract tab, just print to console since we removed the log
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        log_msg = f"{timestamp} {message}"
        print(log_msg)
    def parse_size_from_dropdown(self):
        """Parse selected size string to tuple"""
        size_str = self.size_var.get()
        # Extract numbers from string like "4500 x 5400 px"
        numbers = re.findall(r'\d+', size_str)
        if len(numbers) >= 2:
            return (int(numbers[0]), int(numbers[1]))
        return (4500, 4500)  # Default fallback
        
    def on_size_changed(self, event):
        """Handle size dropdown change"""
        target_size = self.parse_size_from_dropdown()
        self.add_log(f"📐 Output size changed to: {target_size[0]} x {target_size[1]} px @ 300 DPI")
        
        # Check if current image can be re-processed with new size
        if self.current_image_item:
            # Clear the cached result since the fundamental output size has changed
            self.add_log("ℹ️ Output size changed. Image cache cleared for current item.")

            if self.current_image_item and self.current_image_item.status == "completed":
                size_changed = self.current_image_item.processed_size != target_size
                model_changed = self.current_image_item.processed_model != self.upscayl_model_var.get()
                
                if size_changed or model_changed:
                    self.add_log(f"💡 Current image can be re-processed with new settings - click Extract Design")
                else:
                    self.add_log(f"ℹ️  Current image already processed with these settings")
                
    
    
    def on_processing_type_changed(self, event):
        """Handle processing type dropdown change"""
        processing_type = self.processing_type_var.get()
        self.add_log(f"🎯 Selected processing type: {processing_type}")
        
        if processing_type.lower() == "embroidery":
            self.add_log("🧵 Embroidery mode selected - will be developed later")
        else:
            self.add_log("🖨️ Print mode selected - using current processing flow")
    
    def on_mockup_changed(self):
        """Handle mockup checkbox change"""
        if self.mockup_var.get():
            mockup_type = self.mockup_type_var.get()
            self.add_log(f"📱 Mockup mode enabled - {mockup_type} selected")
            # Show model checkbox when mockup is enabled
            self.model_checkbox.pack(side=tk.LEFT, padx=(0, 20))
        else:
            self.add_log("📱 Mockup mode disabled")
            # Hide model checkbox when mockup is disabled
            self.model_checkbox.pack_forget()
            # Reset model checkbox to False
            self.model_var.set(False)
    
    def on_model_changed(self):
        """Handle model checkbox change"""
        if self.model_var.get():
            self.add_log("👤 Model option enabled - mockup will include human model")
        else:
            self.add_log("👤 Model option disabled - mockup will be product-only")
    
    def on_mockup_type_changed(self, event):
        """Handle mockup type dropdown change"""
        mockup_type = self.mockup_type_var.get()
        if self.mockup_var.get():
            self.add_log(f"📱 Mockup type changed to: {mockup_type}")
        # TODO: Update mockup preview if enabled
    
    def on_redesign_changed(self):
        """Handle redesign checkbox change"""
        if self.redesign_var.get():
            self.add_log("🎨 Redesign mode enabled - showing prompt form")
            # Show redesign form
            self.redesign_form_frame.pack(fill=tk.X, pady=(0, 10))
        else:
            self.add_log("🎨 Redesign mode disabled")
            # Hide redesign form
            self.redesign_form_frame.pack_forget()
    
    def get_redesign_prompt(self):
        """Get the redesign prompt from the text widget"""
        prompt = self.redesign_prompt_text.get('1.0', tk.END).strip()
        # Return empty string if it's just the placeholder
        if prompt == self.redesign_prompt_placeholder:
            return ""
        return prompt
    
    def set_redesign_prompt(self, prompt):
        """Set the redesign prompt in the text widget"""
        self.redesign_prompt_text.delete('1.0', tk.END)
        self.redesign_prompt_text.insert('1.0', prompt)
    
    def on_redesign_prompt_focus_in(self, event):
        """Handle focus in event for redesign prompt"""
        if self.redesign_prompt_text.get('1.0', tk.END).strip() == self.redesign_prompt_placeholder:
            self.redesign_prompt_text.delete('1.0', tk.END)
            self.redesign_prompt_text.configure(fg=self.colors['text_white'])
    
    def on_redesign_prompt_focus_out(self, event):
        """Handle focus out event for redesign prompt"""
        if not self.redesign_prompt_text.get('1.0', tk.END).strip():
            self.redesign_prompt_text.insert('1.0', self.redesign_prompt_placeholder)
            self.redesign_prompt_text.configure(fg='#666666')
    
    def on_redesign_prompt_key(self, event):
        """Handle key press event for redesign prompt"""
        if self.redesign_prompt_text.get('1.0', tk.END).strip() == self.redesign_prompt_placeholder:
            self.redesign_prompt_text.delete('1.0', tk.END)
            self.redesign_prompt_text.configure(fg=self.colors['text_white'])
    def process_with_gemini_api(self, image, crop_coordinates=None, target_size=(4500, 4500), upscayl_model='digital-art-4x'):
        """
        Process image using Gemini API for background removal
        """
        def update_progress(value, text):
            if self.processor.progress_callback:
                self.processor.progress_callback(value, text)
        
        try:
            # Validate API key
            api_key = self.gemini_api_key_var.get().strip()
            if not api_key:
                raise ValueError("Gemini API key is required for API mode")
            
            # Initialize Gemini client
            gemini_client = GeminiClient(api_key)
            gemini_model = "gemini-2.5-flash-image-preview"  # Fixed model
            
            self.add_log("🚀 Starting Gemini API processing pipeline...")
            self.processor._check_cancel()
            
            # STEP 0: CROP
            update_progress(5, "Step 0/6: Cropping image...")
            if crop_coordinates:
                x1, y1, x2, y2 = crop_coordinates
                image = image[y1:y2, x1:x2]
                self.add_log(f"✂️ Cropped design area: {image.shape[1]}x{image.shape[0]} px")
            
            # STEP 1: GEMINI API BACKGROUND REMOVAL (no upscaling before API)
            update_progress(15, f"Step 1/6: Processing with Gemini API...")
            
            # Convert image to bytes for API (use original size)
            is_success, buffer = cv2.imencode(".png", image)
            if not is_success:
                raise ValueError("Could not encode image to PNG format.")
            
            # Call Gemini API for design extraction
            self.add_log(f"🤖 Calling Gemini API (gemini-2.5-flash-image-preview)")
            gemini_result = gemini_client.extract_design_with_gemini(buffer.tobytes(), gemini_model, "print")
            
            if gemini_result is None:
                raise RuntimeError("Gemini API failed to process the image")
            
            # Convert PIL image back to OpenCV format
            gemini_array = np.array(gemini_result)
            if len(gemini_array.shape) == 3 and gemini_array.shape[2] == 4:
                # RGBA to BGRA
                removed_bg = cv2.cvtColor(gemini_array, cv2.COLOR_RGBA2BGRA)
            else:
                # Convert to BGRA
                if len(gemini_array.shape) == 3:
                    removed_bg = cv2.cvtColor(gemini_array, cv2.COLOR_RGB2BGRA)
                else:
                    removed_bg = cv2.cvtColor(gemini_array, cv2.COLOR_GRAY2BGRA)
            
            self.add_log("✅ Gemini API processing completed")
            self.processor._check_cancel()
            
            # STEP 2: PHOTOROOM API BACKGROUND REMOVAL (OPTIONAL)
            # Note: PhotoRoom API may change colors, so we'll make it optional
            use_photoroom = True  # Set to True to enable PhotoRoom API
            
            if use_photoroom:
                update_progress(30, "Step 2/5: PhotoRoom API background removal...")
                photoroom_client = PhotoRoomClient()
                photoroom_result = photoroom_client.remove_background(removed_bg)
                
                if photoroom_result is not None:
                    removed_bg = photoroom_result
                    self.add_log("✅ PhotoRoom API background removal completed")
                    
                    # Apply edge sharpening to fix blurred edges
                    removed_bg = self._sharpen_edges(removed_bg)
                    self.add_log("🔧 Applied edge sharpening to fix blurred edges")
                else:
                    self.add_log("⚠️ PhotoRoom API failed, using previous result")
                self.processor._check_cancel()
            else:
                update_progress(30, "Step 2/5: Skipping PhotoRoom API (preserving original colors)...")
                self.add_log("ℹ️ PhotoRoom API disabled to preserve original colors")
            
            # STEP 3: UPSCALE
            update_progress(45, f"Step 3/5: AI Upscaling with {upscayl_model} (4x)...")
            upscaled_image = self.processor._run_ai_upscale(removed_bg, upscayl_model, scale_factor="4")
            self.processor._check_cancel()
            
            # STEP 4: UPSCALE AGAIN
            update_progress(60, f"Step 4/5: AI Upscaling with {upscayl_model} (4x again)...")
            final_upscaled = self.processor._run_ai_upscale(upscaled_image, upscayl_model, scale_factor="4")
            self.processor._check_cancel()
            
            # STEP 5: PLACE ON CANVAS
            update_progress(75, "Step 5/5: Placing on final canvas...")
            final_image = self.processor._place_on_final_canvas(final_upscaled, target_size)
            
            update_progress(100, "✅ Gemini API processing complete!")
            self.add_log("✅ Gemini API processing pipeline completed successfully")
            
            # Record usage for billing
            self.record_image_usage()
            
            return final_image, removed_bg
            
        except Exception as e:
            self.add_log(f"❌ Gemini API processing error: {str(e)}")
            raise
    
    def _sharpen_edges(self, image):
        """
        Aggressive edge sharpening to fix very blurred edges from background removal
        Uses multiple passes and edge reconstruction techniques
        """
        try:
            import cv2
            import numpy as np
            
            # Convert to float32 for processing
            img_float = image.astype(np.float32) / 255.0
            
            # Method 1: Ultra-strong sharpening kernel (7x7)
            ultra_kernel = np.array([[-1, -1, -1, -1, -1, -1, -1],
                                    [-1, -1, -1, -1, -1, -1, -1],
                                    [-1, -1, -1, -1, -1, -1, -1],
                                    [-1, -1, -1, 49, -1, -1, -1],
                                    [-1, -1, -1, -1, -1, -1, -1],
                                    [-1, -1, -1, -1, -1, -1, -1],
                                    [-1, -1, -1, -1, -1, -1, -1]], dtype=np.float32)
            
            # Method 2: High-pass filter for edge enhancement
            high_pass_kernel = np.array([[-1, -1, -1],
                                        [-1,  8, -1],
                                        [-1, -1, -1]], dtype=np.float32)
            
            # Method 3: Sobel edge enhancement
            sobel_x = np.array([[-1, 0, 1],
                               [-2, 0, 2],
                               [-1, 0, 1]], dtype=np.float32)
            
            sobel_y = np.array([[-1, -2, -1],
                               [ 0,  0,  0],
                               [ 1,  2,  1]], dtype=np.float32)
            
            # Apply aggressive sharpening to each channel separately
            if len(img_float.shape) == 3:
                sharpened = np.zeros_like(img_float)
                for i in range(img_float.shape[2]):
                    channel = img_float[:, :, i]
                    
                    if i == 3:  # Alpha channel - keep unchanged
                        sharpened[:, :, i] = channel
                    else:
                        # Step 1: Ultra-strong sharpening
                        ultra_sharp = cv2.filter2D(channel, -1, ultra_kernel * 0.6)
                        
                        # Step 2: High-pass filter
                        high_pass = cv2.filter2D(channel, -1, high_pass_kernel * 0.8)
                        
                        # Step 3: Sobel edge detection and enhancement
                        sobel_x_result = cv2.filter2D(channel, -1, sobel_x)
                        sobel_y_result = cv2.filter2D(channel, -1, sobel_y)
                        sobel_edges = np.sqrt(sobel_x_result**2 + sobel_y_result**2)
                        sobel_edges = np.clip(sobel_edges, 0, 1)
                        
                        # Step 4: Multiple unsharp mask passes
                        gaussian1 = cv2.GaussianBlur(channel, (0, 0), 0.5)
                        gaussian2 = cv2.GaussianBlur(channel, (0, 0), 1.0)
                        gaussian3 = cv2.GaussianBlur(channel, (0, 0), 2.0)
                        
                        unsharp1 = cv2.addWeighted(channel, 2.0, gaussian1, -1.0, 0)
                        unsharp2 = cv2.addWeighted(channel, 1.8, gaussian2, -0.8, 0)
                        unsharp3 = cv2.addWeighted(channel, 1.5, gaussian3, -0.5, 0)
                        
                        # Step 5: Combine all methods aggressively
                        combined = cv2.addWeighted(channel, 0.2, ultra_sharp, 0.4, 0)
                        combined = cv2.addWeighted(combined, 0.6, high_pass, 0.3, 0)
                        combined = cv2.addWeighted(combined, 0.7, unsharp1, 0.2, 0)
                        combined = cv2.addWeighted(combined, 0.8, unsharp2, 0.1, 0)
                        combined = cv2.addWeighted(combined, 0.9, unsharp3, 0.05, 0)
                        
                        # Step 6: Edge-aware sharpening
                        edges = cv2.Canny((channel * 255).astype(np.uint8), 30, 100)
                        edges = cv2.dilate(edges, np.ones((3,3), np.uint8), iterations=1)
                        edges = edges.astype(np.float32) / 255.0
                        
                        # Step 7: Apply sharpening with edge mask
                        sharpened[:, :, i] = cv2.addWeighted(channel, 1 - edges * 0.8, combined, edges * 0.8, 0)
                        
                        # Step 8: Final contrast enhancement
                        sharpened[:, :, i] = np.clip(sharpened[:, :, i] * 1.1, 0, 1)
            else:
                # Grayscale processing
                ultra_sharp = cv2.filter2D(img_float, -1, ultra_kernel * 0.6)
                high_pass = cv2.filter2D(img_float, -1, high_pass_kernel * 0.8)
                
                sobel_x_result = cv2.filter2D(img_float, -1, sobel_x)
                sobel_y_result = cv2.filter2D(img_float, -1, sobel_y)
                sobel_edges = np.sqrt(sobel_x_result**2 + sobel_y_result**2)
                sobel_edges = np.clip(sobel_edges, 0, 1)
                
                gaussian1 = cv2.GaussianBlur(img_float, (0, 0), 0.5)
                gaussian2 = cv2.GaussianBlur(img_float, (0, 0), 1.0)
                gaussian3 = cv2.GaussianBlur(img_float, (0, 0), 2.0)
                
                unsharp1 = cv2.addWeighted(img_float, 2.0, gaussian1, -1.0, 0)
                unsharp2 = cv2.addWeighted(img_float, 1.8, gaussian2, -0.8, 0)
                unsharp3 = cv2.addWeighted(img_float, 1.5, gaussian3, -0.5, 0)
                
                combined = cv2.addWeighted(img_float, 0.2, ultra_sharp, 0.4, 0)
                combined = cv2.addWeighted(combined, 0.6, high_pass, 0.3, 0)
                combined = cv2.addWeighted(combined, 0.7, unsharp1, 0.2, 0)
                combined = cv2.addWeighted(combined, 0.8, unsharp2, 0.1, 0)
                combined = cv2.addWeighted(combined, 0.9, unsharp3, 0.05, 0)
                
                edges = cv2.Canny((img_float * 255).astype(np.uint8), 30, 100)
                edges = cv2.dilate(edges, np.ones((3,3), np.uint8), iterations=1)
                edges = edges.astype(np.float32) / 255.0
                
                sharpened = cv2.addWeighted(img_float, 1 - edges * 0.8, combined, edges * 0.8, 0)
                sharpened = np.clip(sharpened * 1.1, 0, 1)
            
            # Convert back to uint8
            result = (sharpened * 255).astype(np.uint8)
            
            # Ensure alpha channel is preserved correctly
            if len(result.shape) == 3 and result.shape[2] == 4:
                # Keep original alpha channel to preserve transparency
                result[:, :, 3] = image[:, :, 3]
            
            return result
            
        except Exception as e:
            self.add_log(f"⚠️ Edge sharpening failed: {str(e)}, using original image")
            return image
    
    def process_with_gemini_embroidery(self, image, crop_coordinates=None, target_size=(4500, 4500), upscayl_model='digital-art-4x'):
        """
        Process image using Gemini API for embroidery-style design
        Flow: Crop → Gemini API → PhotoRoom Background Removal → Upscale 4x → Place on Canvas
        """
        def update_progress(value, text):
            if self.processor.progress_callback:
                self.processor.progress_callback(value, text)
        
        try:
            # Validate API key
            api_key = self.gemini_api_key_var.get().strip()
            if not api_key:
                raise ValueError("Gemini API key is required for API mode")
            
            # Initialize Gemini client
            gemini_client = GeminiClient(api_key)
            gemini_model = "gemini-2.5-flash-image-preview"  # Fixed model
            
            self.add_log("🧵 Starting Gemini Embroidery processing pipeline...")
            self.processor._check_cancel()
            
            # STEP 0: CROP
            update_progress(10, "Step 0/5: Cropping image...")
            if crop_coordinates:
                x1, y1, x2, y2 = crop_coordinates
                image = image[y1:y2, x1:x2]
                self.add_log(f"✂️ Cropped design area: {image.shape[1]}x{image.shape[0]} px")
            
            # STEP 1: GEMINI API EMBROIDERY PROCESSING
            update_progress(25, "Step 1/5: Processing with Gemini API (Embroidery style)...")
            
            # Convert image to bytes for API (use original size)
            is_success, buffer = cv2.imencode(".png", image)
            if not is_success:
                raise ValueError("Could not encode image to PNG format.")
            
            # Call Gemini API for embroidery processing
            self.add_log(f"🧵 Calling Gemini API for embroidery style (gemini-2.5-flash-image-preview)")
            gemini_result = gemini_client.extract_design_with_gemini(buffer.tobytes(), gemini_model, "embroidery")
            
            if gemini_result is None:
                raise RuntimeError("Gemini API failed to process the image")
            
            # Convert PIL image back to OpenCV format
            gemini_array = np.array(gemini_result)
            if len(gemini_array.shape) == 3 and gemini_array.shape[2] == 4:
                # RGBA to BGRA
                embroidery_design = cv2.cvtColor(gemini_array, cv2.COLOR_RGBA2BGRA)
            else:
                # Convert to BGRA
                if len(gemini_array.shape) == 3:
                    embroidery_design = cv2.cvtColor(gemini_array, cv2.COLOR_RGB2BGRA)
                else:
                    embroidery_design = cv2.cvtColor(gemini_array, cv2.COLOR_GRAY2BGRA)
            
            self.add_log("✅ Gemini API embroidery processing completed")
            self.processor._check_cancel()
            
            # STEP 2: PHOTOROOM BACKGROUND REMOVAL
            update_progress(50, "Step 2/5: Removing background with PhotoRoom API...")
            
            # Debug: Log image info before PhotoRoom
            self.add_log(f"🔍 Before PhotoRoom: Image shape {embroidery_design.shape}, dtype {embroidery_design.dtype}")
            
            photoroom_client = PhotoRoomClient()
            photoroom_result = photoroom_client.remove_background(embroidery_design)
            
            if photoroom_result is not None:
                self.add_log("✅ PhotoRoom background removal completed")
                # Debug: Log image info after PhotoRoom
                self.add_log(f"🔍 After PhotoRoom: Image shape {photoroom_result.shape}, dtype {photoroom_result.dtype}")
                
                # Check if the result actually has transparency
                if len(photoroom_result.shape) == 3 and photoroom_result.shape[2] == 4:
                    alpha_channel = photoroom_result[:, :, 3]
                    unique_alpha = np.unique(alpha_channel)
                    self.add_log(f"🔍 Alpha channel values: {unique_alpha[:10]}...")  # Show first 10 unique values
                    
                    # Count transparent pixels
                    transparent_pixels = np.sum(alpha_channel == 0)
                    total_pixels = alpha_channel.size
                    transparency_ratio = transparent_pixels / total_pixels * 100
                    self.add_log(f"🔍 Transparency: {transparent_pixels}/{total_pixels} pixels ({transparency_ratio:.1f}% transparent)")
                else:
                    self.add_log("⚠️ PhotoRoom result has no alpha channel - no transparency!")
                
                # Debug: Save images for comparison
                try:
                    import tempfile
                    temp_dir = tempfile.gettempdir()
                    
                    # Save before PhotoRoom
                    before_path = os.path.join(temp_dir, "debug_before_photoroom.png")
                    cv2.imwrite(before_path, embroidery_design)
                    self.add_log(f"🔍 Debug: Saved before PhotoRoom to {before_path}")
                    
                    # Save after PhotoRoom
                    after_path = os.path.join(temp_dir, "debug_after_photoroom.png")
                    cv2.imwrite(after_path, photoroom_result)
                    self.add_log(f"🔍 Debug: Saved after PhotoRoom to {after_path}")
                except Exception as e:
                    self.add_log(f"⚠️ Could not save debug images: {e}")
                
                embroidery_design = photoroom_result
            else:
                self.add_log("⚠️ PhotoRoom background removal failed, using original Gemini result")
            
            self.processor._check_cancel()
            
            # STEP 3: EMBROIDERY-SPECIFIC UPSCALING
            update_progress(70, f"Step 3/5: Embroidery upscaling (4x) - preserving stitch details...")
            upscaled_image = self._upscale_embroidery_preserving_details(embroidery_design, scale_factor=4)
            self.processor._check_cancel()
            
            # STEP 4: PLACE ON CANVAS
            update_progress(90, "Step 4/5: Placing on final canvas...")
            final_image = self.processor._place_on_final_canvas(upscaled_image, target_size)
            
            update_progress(100, "✅ Gemini Embroidery processing complete!")
            self.add_log("✅ Gemini Embroidery processing pipeline completed successfully")
            
            # Record usage for billing
            self.record_image_usage()
            
            return final_image, embroidery_design
            
        except Exception as e:
            self.add_log(f"❌ Gemini Embroidery processing error: {str(e)}")
            raise
    
    def process_with_mockup_api(self, image, crop_coordinates=None, target_size=(4500, 4500), upscayl_model='digital-art-4x'):
        """
        Process image using Gemini API for mockup generation
        Flow: Crop → Gemini API → Upscale → Place on Canvas
        """
        def update_progress(value, text):
            if self.processor.progress_callback:
                self.processor.progress_callback(value, text)
        
        try:
            item = self.current_image_item
            mockup_type = self.mockup_type_var.get()
            processing_type = self.processing_type_var.get()
            
            # Get appropriate prompt based on processing type, mockup type, and model option
            self.add_log(f"🔍 Debug - mockup_type: '{mockup_type}'")
            self.add_log(f"🔍 Debug - processing_type: '{processing_type}'")
            self.add_log(f"🔍 Debug - model_enabled: {self.model_var.get()}")
            
            # Choose prompt based on processing type and model option
            if processing_type.lower() == "embroidery":
                if self.model_var.get():
                    prompt = MOCKUP_PROMPTS_EMBROIDERY_MODEL.get(mockup_type, MOCKUP_PROMPTS_EMBROIDERY_MODEL["T-shirt"])
                    self.add_log(f"🔍 Debug - Using EMBROIDERY MODEL prompts")
                else:
                    prompt = MOCKUP_PROMPTS_EMBROIDERY.get(mockup_type, MOCKUP_PROMPTS_EMBROIDERY["T-shirt"])
                    self.add_log(f"🔍 Debug - Using EMBROIDERY prompts")
            else:
                if self.model_var.get():
                    prompt = MOCKUP_PROMPTS_PRINT_MODEL.get(mockup_type, MOCKUP_PROMPTS_PRINT_MODEL["T-shirt"])
                    self.add_log(f"🔍 Debug - Using PRINT MODEL prompts")
                else:
                    prompt = MOCKUP_PROMPTS_PRINT.get(mockup_type, MOCKUP_PROMPTS_PRINT["T-shirt"])
                    self.add_log(f"🔍 Debug - Using PRINT prompts")
            
            model_text = " with model" if self.model_var.get() else ""
            self.add_log(f"📱 Mockup mode: {mockup_type} ({processing_type}){model_text}")
            self.add_log(f"📝 Using prompt: {prompt[:50]}...")
            
            # STEP 1: CROP IMAGE
            update_progress(15, f"Step 1/4: Cropping image for {mockup_type} mockup...")
            if crop_coordinates:
                x1, y1, x2, y2 = crop_coordinates
                cropped_image = image[y1:y2, x1:x2]
                self.add_log(f"✂️ Cropped image to {cropped_image.shape[1]}x{cropped_image.shape[0]}px")
            else:
                cropped_image = image
                self.add_log("ℹ️ No crop coordinates provided, using full image")
            
            self.processor._check_cancel()
            
            # STEP 2: GEMINI API MOCKUP GENERATION
            update_progress(45, f"Step 2/4: Generating {mockup_type} mockup with Gemini API...")
            
            # Initialize Gemini client
            api_key = self.gemini_api_key_var.get().strip()
            gemini_client = GeminiClient(api_key)
            
            # Clear old cache to avoid conflicts with different mockup types
            gemini_client.clear_cache()
            
            # Convert OpenCV image to bytes for Gemini API
            _, buffer = cv2.imencode('.png', cropped_image)
            image_bytes = buffer.tobytes()
            
            # Send to Gemini API with mockup prompt
            gemini_result = gemini_client.extract_design_with_gemini(
                image_bytes, 
                prompt=prompt,
                processing_type="mockup"
            )
            
            if gemini_result is None:
                raise RuntimeError("Gemini API failed to generate mockup")
            
            # Convert PIL image back to OpenCV format
            gemini_array = np.array(gemini_result)
            if len(gemini_array.shape) == 3 and gemini_array.shape[2] == 4:
                # RGBA to BGRA
                mockup_image = cv2.cvtColor(gemini_array, cv2.COLOR_RGBA2BGRA)
            else:
                # Convert to BGRA
                if len(gemini_array.shape) == 3:
                    mockup_image = cv2.cvtColor(gemini_array, cv2.COLOR_RGB2BGRA)
                else:
                    mockup_image = cv2.cvtColor(gemini_array, cv2.COLOR_GRAY2BGRA)
            
            self.add_log("✅ Gemini API mockup generation completed")
            self.processor._check_cancel()
            
            # STEP 3: SCALE TO TARGET SIZE
            update_progress(75, f"Step 3/4: Scaling {mockup_type} mockup to target size...")
            # Scale mockup image to fit target size while maintaining aspect ratio
            h, w = mockup_image.shape[:2]
            target_w, target_h = target_size
            
            # Calculate scale factor to fit within target size
            scale_w = target_w / w
            scale_h = target_h / h
            scale_factor = min(scale_w, scale_h) * 0.9  # 90% of canvas to leave some margin
            
            new_w = int(w * scale_factor)
            new_h = int(h * scale_factor)
            
            scaled_mockup = cv2.resize(mockup_image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
            self.add_log(f"📏 Scaled mockup from {w}x{h} to {new_w}x{new_h} (scale: {scale_factor:.2f})")
            self.processor._check_cancel()
            
            # STEP 4: PLACE ON CANVAS
            update_progress(90, f"Step 4/4: Placing {mockup_type} mockup on final canvas...")
            final_image = self.processor._place_on_final_canvas(scaled_mockup, target_size)
            
            update_progress(100, f"✅ {mockup_type} mockup generation complete!")
            self.add_log(f"✅ {mockup_type} mockup pipeline completed successfully")
            
            # Record usage for billing
            self.record_image_usage()
            
            return final_image, mockup_image
            
        except Exception as e:
            self.add_log(f"❌ Mockup processing error: {str(e)}")
            raise
    
    def process_with_redesign_api(self, image, crop_coordinates=None, target_size=(4500, 4500), upscayl_model='digital-art-4x'):
        """
        Process image using Gemini API for redesign with custom user prompt
        Flow: Crop → Gemini API → PhotoRoom → Upscale 4x → Upscale 4x → Place on Canvas
        """
        def update_progress(value, text):
            if self.processor.progress_callback:
                self.processor.progress_callback(value, text)
        
        try:
            item = self.current_image_item
            processing_type = self.processing_type_var.get()
            user_redesign_prompt = self.get_redesign_prompt()
            
            # Create custom prompt by combining base prompt with user input
            if processing_type.lower() == "embroidery":
                # Embroidery-specific base prompt
                base_prompt = "Như một Designer chuyên nghiệp, hãy thực hiện vẽ lại thiết kế này theo phong cách thêu thực tế trên nền trắng. Thiết kế được khâu bằng len, các đường len thêu ngang, với kết cấu rõ ràng và thể hiện tốt độ sâu 3D. Hiển thị các chi tiết khâu có thể nhìn thấy, bóng nhẹ và độ bóng của sợi để làm cho nó trông thực tế. Với các yêu cầu custom thiết kế sau:"
            else:
                # Print-specific base prompt
                base_prompt = "Như một designer chuyên nghiệp, hãy vẽ lại thiết kế này trên nền xanh lá tươi có độ tương phản cao phù hợp cho việc tách nền. Với các thay đổi sau:"
            
            if user_redesign_prompt:
                custom_prompt = f"{base_prompt} {user_redesign_prompt}"
            else:
                if processing_type.lower() == "embroidery":
                    custom_prompt = f"{base_prompt} Giữ nguyên thiết kế gốc nhưng làm cho nó đẹp hơn và chuyên nghiệp hơn với phong cách thêu."
                else:
                    custom_prompt = f"{base_prompt} Giữ nguyên thiết kế gốc nhưng làm cho nó đẹp hơn và chuyên nghiệp hơn."
            
            self.add_log(f"🎨 Redesign mode: {processing_type}")
            self.add_log(f"📝 Using custom prompt: {custom_prompt[:100]}...")
            
            # STEP 1: CROP IMAGE
            if processing_type.lower() == "embroidery":
                update_progress(10, f"Step 1/4: Cropping image for redesign...")
            else:
                update_progress(10, f"Step 1/6: Cropping image for redesign...")
                
            if crop_coordinates:
                x1, y1, x2, y2 = crop_coordinates
                cropped_image = image[y1:y2, x1:x2]
                self.add_log(f"✂️ Cropped image to {cropped_image.shape[1]}x{cropped_image.shape[0]}px")
            else:
                cropped_image = image
                self.add_log("ℹ️ No crop coordinates provided, using full image")
            
            self.processor._check_cancel()
            
            # STEP 2: GEMINI API REDESIGN
            if processing_type.lower() == "embroidery":
                update_progress(25, f"Step 2/4: Redesigning with Gemini API...")
            else:
                update_progress(20, f"Step 2/6: Redesigning with Gemini API...")
            
            # Initialize Gemini client
            api_key = self.gemini_api_key_var.get().strip()
            gemini_client = GeminiClient(api_key)
            
            # Convert OpenCV image to bytes for Gemini API
            _, buffer = cv2.imencode('.png', cropped_image)
            image_bytes = buffer.tobytes()
            
            # Send to Gemini API with custom redesign prompt
            gemini_result = gemini_client.extract_design_with_gemini(
                image_bytes, 
                prompt=custom_prompt,
                processing_type="redesign"
            )
            
            if gemini_result is None:
                raise RuntimeError("Gemini API failed to redesign")
            
            # Convert PIL image back to OpenCV format
            gemini_array = np.array(gemini_result)
            if len(gemini_array.shape) == 3 and gemini_array.shape[2] == 4:
                # RGBA to BGRA
                redesigned_image = cv2.cvtColor(gemini_array, cv2.COLOR_RGBA2BGRA)
            else:
                # Convert to BGRA
                if len(gemini_array.shape) == 3:
                    redesigned_image = cv2.cvtColor(gemini_array, cv2.COLOR_RGB2BGRA)
                else:
                    redesigned_image = cv2.cvtColor(gemini_array, cv2.COLOR_GRAY2BGRA)
            
            self.add_log("✅ Gemini API redesign completed")
            self.processor._check_cancel()
            
            if processing_type.lower() == "embroidery":
                # EMBROIDERY FLOW: Skip PhotoRoom, only 1 upscale
                
                # STEP 3: UPSCALE (EMBROIDERY)
                update_progress(60, f"Step 3/4: Upscaling redesigned embroidery (4x)...")
                upscaled_image = self.processor._run_ai_upscale(redesigned_image, upscayl_model, scale_factor="4")
                self.processor._check_cancel()
                
                # STEP 4: PLACE ON CANVAS (EMBROIDERY)
                update_progress(90, f"Step 4/4: Placing redesigned embroidery on final canvas...")
                final_image = self.processor._place_on_final_canvas(upscaled_image, target_size)
                
            else:
                # PRINT FLOW: PhotoRoom + 2 upscales
                
                # STEP 3: PHOTOROOM API BACKGROUND REMOVAL
                update_progress(40, f"Step 3/6: Removing background with PhotoRoom API...")
                photoroom_client = PhotoRoomClient()
                photoroom_result = photoroom_client.remove_background(redesigned_image)
                
                if photoroom_result is not None:
                    redesigned_image = photoroom_result
                    self.add_log("✅ PhotoRoom API background removal completed")
                else:
                    self.add_log("⚠️ PhotoRoom API failed, using Gemini result as-is")
                
                self.processor._check_cancel()
                
                # STEP 4: FIRST UPSCALE
                update_progress(60, f"Step 4/6: First upscaling (4x)...")
                upscaled_image = self.processor._run_ai_upscale(redesigned_image, upscayl_model, scale_factor="4")
                self.processor._check_cancel()
                
                # STEP 5: SECOND UPSCALE
                update_progress(80, f"Step 5/6: Second upscaling (4x)...")
                final_upscaled = self.processor._run_ai_upscale(upscaled_image, upscayl_model, scale_factor="4")
                self.processor._check_cancel()
                
                # STEP 6: PLACE ON CANVAS
                update_progress(90, f"Step 6/6: Placing redesigned design on final canvas...")
                final_image = self.processor._place_on_final_canvas(final_upscaled, target_size)
            
            update_progress(100, "✅ Redesign processing complete!")
            self.add_log("✅ Redesign pipeline completed successfully")
            
            # Record usage for billing
            self.record_image_usage()
            
            return final_image, redesigned_image
            
        except Exception as e:
            self.add_log(f"❌ Redesign processing error: {str(e)}")
            raise
    
    def _upscale_embroidery_preserving_details(self, image, scale_factor=4, method="lanczos"):
        """
        Upscale embroidery design while preserving stitch details and sharp edges
        Uses specialized techniques to maintain the characteristic look of embroidery
        
        Args:
            image: Input image
            scale_factor: Scale factor for upscaling
            method: "lanczos" (default), "nearest", "bicubic", "hybrid"
        """
        try:
            import cv2
            import numpy as np
            
            self.add_log(f"🧵 Applying embroidery-specific upscaling (x{scale_factor}) using {method} method...")
            
            height, width = image.shape[:2]
            new_height, new_width = height * scale_factor, width * scale_factor
            
            # Method 1: Lanczos (best for preserving fine details like stitches)
            if method == "lanczos":
                result = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
                self.add_log(f"✅ Embroidery upscaling completed using Lanczos (preserves stitch details)")
                return result
            
            # Method 2: Nearest Neighbor (preserves pixel-perfect sharp edges)
            elif method == "nearest":
                result = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_NEAREST)
                self.add_log(f"✅ Embroidery upscaling completed using Nearest Neighbor (sharp edges)")
                return result
            
            # Method 3: Bicubic (smooth but may blur stitches)
            elif method == "bicubic":
                result = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
                self.add_log(f"✅ Embroidery upscaling completed using Bicubic")
                return result
            
            # Method 4: Hybrid approach (combines multiple methods)
            elif method == "hybrid":
                # Step 1: Lanczos for overall quality
                lanczos_result = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
                
                # Step 2: Nearest neighbor for sharp edges
                nearest_result = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_NEAREST)
                
                # Step 3: Detect stitch areas using edge detection
                if len(image.shape) == 3:
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                else:
                    gray = image.copy()
                
                # Detect edges (stitch boundaries)
                edges = cv2.Canny(gray, 30, 100)
                edges_upscaled = cv2.resize(edges, (new_width, new_height), interpolation=cv2.INTER_NEAREST)
                
                # Create mask for stitch areas
                stitch_mask = (edges_upscaled > 0).astype(np.float32)
                if len(image.shape) == 3:
                    stitch_mask = np.stack([stitch_mask] * 3, axis=2)
                
                # Blend: Lanczos for smooth areas, Nearest for stitch areas
                result = (lanczos_result * (1 - stitch_mask) + nearest_result * stitch_mask).astype(np.uint8)
                
                # Step 4: Apply slight sharpening to enhance stitch definition
                sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                if len(result.shape) == 3:
                    sharpened = cv2.filter2D(result, -1, sharpen_kernel)
                else:
                    sharpened = cv2.filter2D(result, -1, sharpen_kernel)
                
                # Final blend: 80% hybrid + 20% sharpened
                result = (result * 0.8 + sharpened * 0.2).astype(np.uint8)
                
                self.add_log(f"✅ Embroidery upscaling completed using Hybrid method (optimal stitch preservation)")
                return result
            
            # Default fallback
            else:
                result = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
                self.add_log(f"✅ Embroidery upscaling completed using default Lanczos")
                return result
            
        except Exception as e:
            self.add_log(f"⚠️ Embroidery upscaling error, falling back to standard upscaling: {str(e)}")
            # Fallback to standard bicubic if custom method fails
            height, width = image.shape[:2]
            new_height, new_width = height * scale_factor, width * scale_factor
            return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
            
        
    def update_processed_list(self):
        """Update processed results list with checkboxes"""
        # Clear existing processed list
        for widget in self.processed_list_container.winfo_children():
            widget.destroy()
            
        # Get completed items
        completed_items = [item for item in self.image_items if item.status == "completed"]
        
        if not completed_items:
            # Show empty state
            empty_label = tk.Label(self.processed_list_container, 
                                 text="No processed images yet\nExtract designs to see results here",
                                 bg=self.colors['bg_dark'],
                                 fg=self.colors['text_gray'],
                                 font=('Arial', 10),
                                 justify=tk.CENTER)
            empty_label.pack(expand=True)
            return
            
        # Add scrollable area for processed items
        canvas = Canvas(self.processed_list_container, bg=self.colors['bg_dark'])
        scrollbar = Scrollbar(self.processed_list_container, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=self.colors['bg_dark'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add checkbox for each processed image
        for i, item in enumerate(completed_items):
            item_frame = Frame(scrollable_frame, bg=self.colors['bg_dark'])
            item_frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Checkbox for download selection
            var = tk.BooleanVar(value=item.selected_for_download)
            checkbox = tk.Checkbutton(item_frame, variable=var,
                                    bg=self.colors['bg_dark'],
                                    fg=self.colors['text_white'],
                                    selectcolor=self.colors['bg_medium'],
                                    command=lambda idx=i, v=var, it=item: self.on_processed_item_toggle(it, v))
            checkbox.pack(side=tk.LEFT)
            
            # Image info with size and rotation
            if item.processed_size:
                w, h = item.processed_size
                model_name = item.processed_model or "N/A"
                size_text = f" ({w}x{h}px"
                size_text += f", {model_name})"
            else:
                size_text = ""
                
            label_text = f"✅ {item.filename}{size_text}"
            
            label = tk.Label(item_frame, text=label_text,
                           bg=self.colors['bg_dark'],
                           fg=self.colors['text_white'],
                           font=('Arial', 9),
                           anchor='w')
            label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
            
            # Click to preview
            label.bind("<Button-1>", lambda e, it=item: self.preview_processed_image(it))
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def select_all_download(self):
        """Select all processed images for download"""
        completed_items = [item for item in self.image_items if item.status == "completed"]
        for item in completed_items:
            item.selected_for_download = True
        self.update_processed_list()
        self.add_log(f"💾 Selected all {len(completed_items)} processed images for download")
        
    def select_none_download(self):
        """Deselect all processed images for download"""
        completed_items = [item for item in self.image_items if item.status == "completed"]
        for item in completed_items:
            item.selected_for_download = False
        self.update_processed_list()
        self.add_log(f"💾 Cleared download selection")
        
    def on_processed_item_toggle(self, item, var):
        """Handle processed item checkbox toggle"""
        item.selected_for_download = var.get()
        selected_count = sum(1 for it in self.image_items if it.status == "completed" and it.selected_for_download)
        total_count = sum(1 for it in self.image_items if it.status == "completed")
        self.add_log(f"💾 Download selection: {selected_count}/{total_count} images selected")
        
    def preview_processed_image(self, item):
        """Preview processed image on canvas"""
        if item.processed_image is not None:
            self.current_image_item = item
            self.load_image_to_canvas(item)
            self.display_extracted_result(item.processed_image)
            
            if item.processed_size:
                w, h = item.processed_size
                model_name = item.processed_model or "N/A"
                self.add_log(f"👁️ Previewing: {item.filename} ({w}x{h}px, {model_name})")
            else:
                self.add_log(f"👁️ Previewing: {item.filename}")
            
            self.update_file_count()

        
    def update_image_list_display(self):
        """Update image list display"""
        self.add_log(f"🔄 Updating display: images={len(self.image_items)}")
        
        # Always show single image mode
        self.image_listbox.pack_forget()
        # Create single mode frame if it doesn't exist
        if not hasattr(self, 'single_list_frame'):
            self.single_list_frame = Frame(self.list_container, bg=self.colors['bg_dark'])
        
        self.single_list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Clear and rebuild single mode list
        for widget in self.single_list_frame.winfo_children():
            widget.destroy()
        # Add scrollable area for single items
        canvas = Canvas(self.single_list_frame, bg=self.colors['bg_dark'])
        scrollbar = Scrollbar(self.single_list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=self.colors['bg_dark'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add item for each image
        for i, item in enumerate(self.image_items):
            item_frame = Frame(scrollable_frame, bg=self.colors['bg_dark'])
            item_frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Image name with status
            status_icon = "✅" if item.status == "completed" else "⏳" if item.status == "processing" else "📷"
            label_text = f"{status_icon} {item.filename}"
            
            label = tk.Label(item_frame, text=label_text,
                           bg=self.colors['bg_dark'],
                           fg=self.colors['text_white'],
                           font=('Arial', 9),
                           anchor='w')
            label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
            
            # Click to view image
            label.bind("<Button-1>", lambda e, idx=i: self.on_single_item_click(idx))
            
            # Delete button (X icon) - text only, no background, no border
            delete_btn = tk.Label(item_frame, text="×", 
                                 bg=self.colors['bg_dark'], fg='#ff4444',
                                 font=('Arial', 12, 'bold'),
                                 cursor="hand2")
            delete_btn.pack(side=tk.RIGHT, padx=(0, 5))
            delete_btn.bind("<Button-1>", lambda e, idx=i: self.delete_single_image(idx))
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
                
        if self.current_image_item:
            if self.current_image_item.status == "completed" and self.current_image_item.processed_size:
                w, h = self.current_image_item.processed_size
                self.add_log(f"📋 Viewing: {self.current_image_item.filename} (processed at {w}x{h}px)")
            else:
                self.add_log(f"📋 Viewing: {self.current_image_item.filename}")
        
        self.update_file_count()
    
    def on_single_item_click(self, index):
        """Handle clicking on single item label to view"""
        self.current_image_item = self.image_items[index]
        self.load_image_to_canvas(self.current_image_item)
        
        if self.current_image_item and self.current_image_item.status == "completed" and self.current_image_item.processed_size:
            w, h = self.current_image_item.processed_size
            self.add_log(f"📋 Viewing: {self.current_image_item.filename} (processed at {w}x{h}px)")
        else:
            self.add_log(f"📋 Viewing: {self.current_image_item.filename} (not processed yet)")
        
        self.update_file_count()
    
    def delete_single_image(self, index):
        """Delete a single image from the list"""
        try:
            if index < 0 or index >= len(self.image_items):
                return
                
            item = self.image_items[index]
            filename = item.filename
            
            # If this is the current image, clear it
            if self.current_image_item == item:
                self.current_image_item = None
                self.original_canvas.delete("all")
                self.extracted_canvas.delete("all")
                self._draw_checkerboard_background()
                
                # Clear extracted image for video generation
                if hasattr(self, 'extracted_image'):
                    self.extracted_image = None
            
            # Remove from list
            self.image_items.pop(index)
            
            # Update displays
            self.update_image_list_display()
            self.update_processed_list()
            self.update_file_count()
            
            self.add_log(f"🗑️ Deleted: {filename}")
            
        except Exception as e:
            self.add_log(f"❌ Error deleting image: {str(e)}")
        
    def verify_dpi(self, file_path):
        """Verify that saved file has correct DPI"""
        try:
            with Image.open(file_path) as img:
                dpi = img.info.get('dpi', (72, 72))  # Default to 72 if no DPI info
                return dpi == (300, 300) or dpi == (300.0, 300.0)
        except:
            return False
        

            
    def browse_files(self):
        """Browse and add image files"""
        file_types = [
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp"),
            ("All files", "*.*")
        ]
        
        filenames = filedialog.askopenfilenames(
            title="Select images to process",
            filetypes=file_types
        )
        
        if filenames:
            self.add_image_files(filenames)
            
    def add_image_files(self, file_paths):
        """Add image files to the list"""
        for file_path in file_paths:
            if len(self.image_items) >= 10:
                messagebox.showwarning("Limit Reached", "Maximum 10 images allowed!")
                break
                
            try:
                with Image.open(file_path) as img:
                    item = ImageItem(file_path)
                    self.image_items.append(item)
                    self.add_log(f"📁 Added: {item.filename}")
            except Exception as e:
                self.add_log(f"❌ Error loading {os.path.basename(file_path)}: {str(e)}")
                
        self.update_image_list_display()
        self.update_processed_list()
        self.update_file_count()
        
    def update_file_count(self):
        """Update file count display"""
        count = len(self.image_items)
        completed_count = len([item for item in self.image_items if item.status == "completed"])
        download_selected = sum(1 for item in self.image_items if item.status == "completed" and item.selected_for_download)
        
        # Show batch, download, or current image status
        status_parts = []
        
        # Show current image status
        if self.current_image_item and self.current_image_item.status == "completed":
            if self.current_image_item.processed_size:
                w, h = self.current_image_item.processed_size
                status_parts.append(f"Current: {w}x{h}px")
        
        # Always show download selection if there are completed items
        if completed_count > 0:
            status_parts.append(f"Download: {download_selected}/{completed_count}")
        
        # File count label removed - no longer needed
        
    def clear_all(self):
        """Clear all images"""
        self.image_items.clear()
        self.current_image_item = None
        self.original_canvas.delete("all")
        self.extracted_canvas.delete("all")
        self._draw_checkerboard_background()
        
        # Clear extracted image for video generation
        if hasattr(self, 'extracted_image'):
            self.extracted_image = None
            
        self.update_image_list_display()
        self.update_processed_list()
        self.update_file_count()
        self.add_log("🗑️ Cleared all images")
        
    def on_image_select(self, event):
        """Handle image selection from list"""
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.current_image_item = self.image_items[index]
            self.load_image_to_canvas(self.current_image_item)
            
            # Show status of selected image
            if self.current_image_item and self.current_image_item.status == "completed" and self.current_image_item.processed_size:
                w, h = self.current_image_item.processed_size
                processed_rotation = self.current_image_item.processed_rotation or 0
                current_size = self.parse_size_from_dropdown()
                current_model = self.upscayl_model_var.get()
                
                size_match = (w, h) == current_size
                model_match = self.current_image_item.processed_model == current_model
                
                if size_match and model_match:
                    self.add_log(f"📋 Selected: {self.current_image_item.filename} (already processed with current settings)")
                else:
                    self.add_log(f"📋 Selected: {self.current_image_item.filename} (processed, but settings differ - can re-process)")
            else:
                self.add_log(f"📋 Selected: {self.current_image_item.filename} (not processed yet)")
            
            # Update file count to show current image status
            self.update_file_count()
            
    def load_image_to_canvas(self, item):
        """Load image to original canvas"""
        try:
            # Load and resize image for display
            original_img = Image.open(item.file_path)
            
            # Calculate size to fit canvas
            canvas_width = self.original_canvas.winfo_width()
            canvas_height = self.original_canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:  # Canvas is initialized
                # Calculate scale factor to fit image in canvas
                scale_x = (canvas_width - 20) / original_img.width
                scale_y = (canvas_height - 20) / original_img.height
                scale_factor = min(scale_x, scale_y)
                
                # Calculate display size
                display_width = int(original_img.width * scale_factor)
                display_height = int(original_img.height * scale_factor)
                
                # Calculate offset to center image
                offset_x = (canvas_width - display_width) // 2
                offset_y = (canvas_height - display_height) // 2
                
                # Store canvas info for coordinate conversion
                self.canvas_image_info = {
                    'scale_factor': scale_factor,
                    'offset_x': offset_x,
                    'offset_y': offset_y,
                    'display_width': display_width,
                    'display_height': display_height,
                    'original_width': original_img.width,
                    'original_height': original_img.height
                }
                
                # Resize image for display
                display_img = original_img.copy()
                display_img.thumbnail((display_width, display_height), Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(display_img)
                
                # Clear canvas and display image
                self.original_canvas.delete("all")
                self.original_canvas.create_image(
                    canvas_width//2, canvas_height//2, 
                    image=photo, anchor=tk.CENTER
                )
                self.original_canvas.image = photo  # Keep reference
                
                self.add_log(f"🖼️ Loaded: {item.filename}")
                
                # Display extracted result if available
                if item.processed_image is not None:
                    self.display_extracted_result(item.processed_image)
                else:
                    # Clear extracted canvas if no result and show checkerboard
                    self.extracted_canvas.delete("all")
                    self._draw_checkerboard_background()
                
        except Exception as e:
            self.add_log(f"❌ Error displaying {item.filename}: {str(e)}")
            
    def display_extracted_result(self, processed_image):
        """Display processed result on extracted canvas"""
        try:
            # Convert BGRA to RGBA for proper transparency handling
            rgba_img = cv2.cvtColor(processed_image, cv2.COLOR_BGRA2RGBA)
            pil_img = Image.fromarray(rgba_img)
            
            # Store original image for zoom functionality
            self.set_current_zoom_image(processed_image)
            
            # Store extracted image for video generation
            self.extracted_image = pil_img.copy()
            
            # Calculate size to fit canvas
            canvas_width = self.extracted_canvas.winfo_width()
            canvas_height = self.extracted_canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:  # Canvas is initialized
                pil_img.thumbnail((canvas_width-20, canvas_height-20), Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage with transparency support
                photo = ImageTk.PhotoImage(pil_img)
                
                # Clear canvas and redraw checkerboard background
                self.extracted_canvas.delete("all")
                self._draw_checkerboard_background()
                
                # Display result on top of checkerboard
                self.extracted_canvas.create_image(
                    canvas_width//2, canvas_height//2, 
                    image=photo, anchor=tk.CENTER
                )
                self.extracted_canvas.image = photo  # Keep reference
                
                self.add_log("✨ Result displayed on transparent background")
                # Increment designs_extracted usage
                try:
                        self.load_usage_stats()
                except Exception:
                    pass
            else:
                # Canvas not ready, try again after a short delay
                self.root.after(100, lambda: self.display_extracted_result(processed_image))
                
        except Exception as e:
            self.add_log(f"❌ Error displaying result: {str(e)}")
             
    def on_canvas_configure(self, event):
        """Handle canvas resize - refresh current image if any"""
        if hasattr(self, 'current_image_item') and self.current_image_item:
            # Delay refresh to avoid too many calls during resize
            if hasattr(self, '_resize_after_id'):
                self.root.after_cancel(self._resize_after_id)
            self._resize_after_id = self.root.after(100, self.refresh_canvas_images)
    
    def refresh_canvas_images(self):
        """Refresh images on canvas after resize"""
        if self.current_image_item:
            self.load_image_to_canvas(self.current_image_item)
             
    def start_selection(self, event):
        """Start rectangle selection"""
        self.selection_start = (event.x, event.y)
        
    def update_selection(self, event):
        """Update rectangle selection"""
        if self.selection_start:
            if self.selection_rect:
                self.original_canvas.delete(self.selection_rect)
                
            self.selection_rect = self.original_canvas.create_rectangle(
                self.selection_start[0], self.selection_start[1],
                event.x, event.y,
                outline="red", width=2, stipple="gray25"
            )
            
    def end_selection(self, event):
        """End rectangle selection"""
        if self.selection_start and self.current_image_item:
            self.selection_end = (event.x, event.y)
            
            # Convert canvas coordinates to actual image coordinates
            self.convert_selection_to_image_coords()
            if self.current_image_item.crop_coordinates:
                x1, y1, x2, y2 = self.current_image_item.crop_coordinates
                self.add_log(f"✂️ Selected region: {x2-x1}x{y2-y1} px")
            else:
                                self.add_log("✂️ Selection area defined")
              
    def convert_selection_to_image_coords(self):
        """Convert canvas selection coordinates to original image coordinates"""
        if not self.selection_start or not self.selection_end or not self.current_image_item:
            return
            
        # Get canvas coordinates
        canvas_x1 = min(self.selection_start[0], self.selection_end[0])
        canvas_y1 = min(self.selection_start[1], self.selection_end[1]) 
        canvas_x2 = max(self.selection_start[0], self.selection_end[0])
        canvas_y2 = max(self.selection_start[1], self.selection_end[1])
        
        # Get canvas and image info
        info = self.canvas_image_info
        
        # Convert canvas coordinates to image coordinates
        # Remove offset and scale back to original size
        img_x1 = max(0, int((canvas_x1 - info['offset_x']) / info['scale_factor']))
        img_y1 = max(0, int((canvas_y1 - info['offset_y']) / info['scale_factor']))
        img_x2 = min(info['original_width'], int((canvas_x2 - info['offset_x']) / info['scale_factor']))
        img_y2 = min(info['original_height'], int((canvas_y2 - info['offset_y']) / info['scale_factor']))
        
        # Ensure valid selection
        if img_x2 > img_x1 and img_y2 > img_y1:
            self.current_image_item.crop_coordinates = (img_x1, img_y1, img_x2, img_y2)
            self.add_log(f"📐 Design area selected: {img_x2-img_x1}x{img_y2-img_y1} px")
        else:
            self.add_log("❌ Invalid selection area")
            self.current_image_item.crop_coordinates = None
              
    def clear_selection(self):
        """Clear current selection"""
        if self.selection_rect:
            self.original_canvas.delete(self.selection_rect)
            self.selection_rect = None
        self.selection_start = None
        self.selection_end = None
        
        # Clear crop coordinates from current item
        if self.current_image_item:
            self.current_image_item.crop_coordinates = None
 # <-- Invalidate cache
            
        self.add_log("🗑️ Selection cleared")
    
    def on_right_click(self, event):
        """Handle right-click on canvas for context menu"""
        # Create context menu
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="Paste Image from Clipboard", command=self.paste_from_clipboard)
        context_menu.add_separator()
        context_menu.add_command(label="Browse Files...", command=self.browse_files)
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    def paste_from_clipboard(self):
        """Paste image from clipboard"""
        try:
            # Try to get image from clipboard using PIL
            from PIL import ImageGrab
            image = ImageGrab.grabclipboard()
            if image:
                # Save to temporary file
                import tempfile
                temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                image.save(temp_file.name)
                temp_file.close()
                
                self.add_image_files([temp_file.name])
                self.add_log("📋 Pasted image from clipboard")
                # Auto-select the pasted image
                self.auto_select_pasted_image(temp_file.name)
                return
            
            # Try to get file path from clipboard
            try:
                clipboard_data = self.root.clipboard_get()
                if os.path.exists(clipboard_data):
                    if clipboard_data.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                        self.add_image_files([clipboard_data])
                        self.add_log(f"📋 Pasted image from clipboard: {os.path.basename(clipboard_data)}")
                        self.auto_select_pasted_image(clipboard_data)
                        return
            except tk.TclError:
                pass
                
            self.add_log("❌ No valid image found in clipboard")
            
        except Exception as e:
            self.add_log(f"❌ Error pasting from clipboard: {str(e)}")
    
    def auto_select_pasted_image(self, file_path):
        """Auto-select the pasted image and load it to canvas"""
        try:
            # Find the image item that was just added
            for item in self.image_items:
                if item.file_path == file_path:
                    self.current_image_item = item
                    self.load_image_to_canvas(item)
                    self.update_file_count()
                    self.update_image_list_display()
                    self.add_log(f"🎯 Auto-selected pasted image: {item.filename}")
                    return
        except Exception as e:
            self.add_log(f"❌ Error auto-selecting pasted image: {str(e)}")
    
        
    def extract_current_design(self):
        """
        Handles both starting and canceling the processing task.
        Acts as a toggle button.
        """
        if self.is_processing:
            self.cancel_processing()
            return

            # Single mode - process current image
            if not self.current_image_item:
                messagebox.showwarning("No Image Selected", "Please select an image first!")
                return
                
        # Check API key
        api_key = self.gemini_api_key_var.get().strip()
        if not api_key:
            messagebox.showwarning("API Key Required", "Gemini API key is not configured!")
            return
        
        # Test connection first
        try:
            client = GeminiClient(api_key)
            if not client.test_connection():
                messagebox.showerror("API Connection Failed", "Cannot connect to Gemini API. Please check the connection!")
                return
        except Exception as e:
            messagebox.showerror("API Error", f"Error testing Gemini API: {str(e)}")
            return
        
        # Get processing type and start full processing
        processing_type = self.processing_type_var.get()
        mode_text = f" (API mode: {processing_type})"
        self.add_log(f"🔄 Starting full processing pipeline...{mode_text}")
        thread = threading.Thread(target=self.process_current_image)
        thread.daemon = True
        thread.start()

    def cancel_processing(self):
        """Signals the processing thread to stop."""
        if self.is_processing:
            self.add_log("🛑 Cancel signal sent. Waiting for current step to finish...")
            self.cancel_event.set()
            # The button state will be reset by the processing thread itself.

    def show_progress_ui(self, show=True):
        """Show or hide the progress bar UI."""
        if show:
            self.extracted_canvas.pack_forget()
            self.progress_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            self.start_gif_animation()
        else:
            self.stop_gif_animation()
            self.progress_frame.pack_forget()
            self.extracted_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
    def update_progress(self, value, text):
        """Callback to update progress bar from the processing thread."""
        self.progress_bar['value'] = value
        self.progress_label['text'] = text
        self.root.update_idletasks()
        
    def process_current_image(self):
        """Process current selected image in background thread (FULL PIPELINE)"""
        self.is_processing = True
        self.cancel_event.clear()
        
        # Setup processor with callbacks
        self.processor.progress_callback = self.update_progress
        self.processor.cancel_event = self.cancel_event
        
        self.root.after(0, lambda: self.extract_btn.configure(text="Cancel", bg=self.colors['error']))
        self.root.after(0, lambda: self.show_progress_ui(True))
        
        try:
            item = self.current_image_item
            
            # Get selected target size and model settings
            target_size = self.parse_size_from_dropdown()
            upscayl_model = self.upscayl_model_var.get()
            processing_type = self.processing_type_var.get()
            
            # Determine mode text
            if self.mockup_var.get():
                mockup_type = self.mockup_type_var.get()
                model_text = " + Model" if self.model_var.get() else ""
                mode_text = f" (Mockup mode: {mockup_type} - {processing_type}{model_text})"
            elif self.redesign_var.get():
                mode_text = f" (Redesign mode: {processing_type})"
            else:
                mode_text = f" (API mode: {processing_type})"
            
            self.add_log(f"🔄 Processing: {item.filename} → {target_size[0]}x{target_size[1]}px with '{upscayl_model}'{mode_text}")
            
            # Read image
            image = cv2.imread(item.file_path)
            if image is None:
                raise IOError(f"Cannot read image file: {item.filename}")
            
            # Check processing mode
            if self.mockup_var.get():
                # Mockup flow: Crop → Gemini API → Scale → Place on Canvas
                processed, removed_bg = self.process_with_mockup_api(image, item.crop_coordinates, target_size, upscayl_model)
            elif self.redesign_var.get():
                # Redesign flow: Crop → Gemini API → PhotoRoom → Upscale 4x → Upscale 4x → Place on Canvas
                processed, removed_bg = self.process_with_redesign_api(image, item.crop_coordinates, target_size, upscayl_model)
            elif processing_type.lower() == "embroidery":
                # Embroidery flow: Crop → Gemini API → Upscale 4x → Place on Canvas
                processed, removed_bg = self.process_with_gemini_embroidery(image, item.crop_coordinates, target_size, upscayl_model)
            else:
                # Print flow: Crop → Gemini API → PhotoRoom → Upscale 4x → Upscale 4x → Place on Canvas
                processed, removed_bg = self.process_with_gemini_api(image, item.crop_coordinates, target_size, upscayl_model)
            
            if self.cancel_event.is_set():
                item.status = "pending"
                self.add_log(f"🛑 Process for {item.filename} was cancelled.")
            elif processed is not None:
                item.processed_image = processed
                item.status = "completed"
                item.processed_size = target_size
                item.processed_model = upscayl_model

                # Store params to check against for cache invalidation
                self.last_processed_params = {
                    'crop': item.crop_coordinates,
                    'model': upscayl_model,
                    'size': target_size
                }

                self.root.after(0, lambda img=processed: self.display_extracted_result(img))
                self.add_log(f"✅ Completed: {item.filename}")
            else:
                raise RuntimeError("Processing failed for an unknown reason.")

        except Exception as e:
            item.status = "error"
            self.add_log(f"❌ Processing error for {item.filename}: {str(e)}")
            messagebox.showerror("Processing Error", f"An error occurred while processing {item.filename}:\n\n{e}")
        finally:
            self.is_processing = False
            self.root.after(0, self.show_progress_ui, False)
            self.root.after(0, self.update_image_list_display)
            self.root.after(0, self.update_processed_list)
            self.root.after(0, self.update_file_count)
            
            # Reset button state
            self.root.after(0, lambda: self.extract_btn.configure(text="Extract Design", bg='#90ee90'))
            
            
    def save_results(self):
        """Save selected processed results"""
        # Get selected completed items
        selected_items = [item for item in self.image_items if item.status == "completed" and item.selected_for_download]
        
        if not selected_items:
            completed_count = len([item for item in self.image_items if item.status == "completed"])
            if completed_count == 0:
                messagebox.showinfo("No Results", "No processed images to save!\nPlease process some images first.")
            else:
                messagebox.showinfo("No Selection", f"No images selected for download!\nYou have {completed_count} processed images.\nSelect them in 'Processed Results' section first.")
            return
            
        success_count = 0
        for item in selected_items:
            try:
                # Get dimensions from processed size (more reliable than image shape)
                if item.processed_size:
                    w, h = item.processed_size
                else:
                    # Fallback to image shape if processed_size not available
                    h, w = item.processed_image.shape[:2]
                
                model_suffix = item.processed_model or "unknown_model"
                size_suffix = f"{w}x{h}_{model_suffix}"
                
                # Generate default filename
                default_filename = f"{Path(item.filename).stem}_extracted_{size_suffix}.png"
                
                # Ask user to choose save location and filename for each file
                save_path = filedialog.asksaveasfilename(
                    title=f"Save extracted design: {Path(item.filename).name}",
                    initialfile=default_filename,
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
                )
                
                if not save_path:
                    # User cancelled this file, continue with next file
                    continue
                
                pil_output = Image.fromarray(cv2.cvtColor(item.processed_image, cv2.COLOR_BGRA2RGBA))
                
                # Ensure 300 DPI is always set for all sizes
                pil_output.save(save_path, format='PNG', dpi=(300, 300), optimize=True)
                
                # Verify DPI was set correctly
                if self.verify_dpi(save_path):
                    dpi_status = "✅ 300 DPI verified"
                else:
                    dpi_status = "⚠️  DPI verification failed"
                
                success_count += 1
                self.add_log(f"💾 Saved: {Path(save_path).name} ({w}x{h}px @ 300 DPI) - {dpi_status}")
            except Exception as e:
                self.add_log(f"❌ Save error for {item.filename}: {str(e)}")
                
        if success_count > 0:
            messagebox.showinfo("Save Complete", 
                               f"Successfully saved {success_count}/{len(selected_items)} selected images @ 300 DPI")
        else:
            messagebox.showinfo("Save Cancelled", "No files were saved.")

    def on_right_click_extracted(self, event):
        """Handle right-click press on extracted canvas"""
        # Store initial position and reset dragging state
        self.right_click_start_pos = (event.x, event.y)
        self.is_dragging = False
        
        # Start zoom preview immediately for smooth experience
        if hasattr(self, 'current_zoom_image') and self.current_zoom_image is not None:
            self.start_zoom_preview(event)

    def on_right_drag_extracted(self, event):
        """Handle right-click drag on extracted canvas"""
        if self.right_click_start_pos:
            # Calculate distance moved
            start_x, start_y = self.right_click_start_pos
            distance = ((event.x - start_x) ** 2 + (event.y - start_y) ** 2) ** 0.5
            
            # If moved more than 5 pixels, consider it dragging
            if distance > 5:
                self.is_dragging = True
                
            # Update zoom preview if dragging
            if self.is_dragging and hasattr(self, 'current_zoom_image') and self.current_zoom_image is not None:
                self.update_zoom_preview(event)

    def on_right_release_extracted(self, event):
        """Handle right-click release on extracted canvas"""
        try:
            if self.is_dragging:
                # Was dragging - end zoom preview
                self.end_zoom_preview(event)
            else:
                # Was just a click - show context menu
                self.show_extracted_context_menu(event)
        finally:
            # Reset state
            self.right_click_start_pos = None
            self.is_dragging = False

    def show_extracted_context_menu(self, event):
        """Show context menu for extracted design canvas"""
        # Only show menu if there's an extracted image
        if not hasattr(self, 'extracted_image') or self.extracted_image is None:
            return
            
        # Create context menu
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="🎬 Video Generate", 
                               command=self.send_to_video_gen)
        context_menu.add_separator()
        context_menu.add_command(label="🔍 Zoom Preview", 
                               command=lambda: self.start_zoom_preview(event))
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def send_to_video_gen(self):
        """Send extracted design to Video Gen tab"""
        try:
            if not hasattr(self, 'extracted_image') or self.extracted_image is None:
                messagebox.showwarning("Warning", "No extracted design to send to Video Gen")
                return
            
            # Save extracted image to a temporary file
            import tempfile
            import os
            
            # Create temp file
            temp_dir = tempfile.gettempdir()
            temp_filename = f"extracted_for_video_{int(time.time())}.png"
            temp_path = os.path.join(temp_dir, temp_filename)
            
            # Save extracted image
            self.extracted_image.save(temp_path, "PNG")
            
            # Switch to Video Gen tab
            self.show_page("video_gen")
            
            # Load image into Video Gen
            self.video_gen_image_path = temp_path
            self.video_gen_original_image = self.extracted_image.copy()
            self._display_uploaded_image()
            
            # Add log message
            self.add_video_gen_log(f"📤 Loaded extracted design from Extract tab")
            self.add_video_gen_log("Ready to generate video. Click 'Generate Video' button.")
            
            messagebox.showinfo("Success", "Extracted design loaded into Video Gen tab!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send to Video Gen: {str(e)}")

    def start_zoom_preview(self, event):
        """Start zoom preview when right-clicking on extracted canvas"""
        if not hasattr(self, 'current_zoom_image') or self.current_zoom_image is None:
            return
        
        # Update zoom preview
        self.update_zoom_preview(event)
    
    def update_zoom_preview(self, event):
        """Update zoom preview based on mouse position"""
        if self.current_zoom_image is None:
            return
            
        try:
            # Get mouse position relative to extracted canvas
            canvas_x = self.extracted_canvas.canvasx(event.x)
            canvas_y = self.extracted_canvas.canvasy(event.y)
            
            # Get canvas dimensions
            canvas_width = self.extracted_canvas.winfo_width()
            canvas_height = self.extracted_canvas.winfo_height()
            
            # Calculate zoom area (800x800 pixels around mouse - very large magnifying glass)
            zoom_size = 800
            zoom_factor = 0.2  # 0.2x zoom (smaller image inside magnifying glass)
            
            # Calculate source coordinates in the original image
            if hasattr(self, 'extracted_canvas') and self.extracted_canvas.image:
                # Get the displayed image dimensions
                img_width = self.extracted_canvas.image.width()
                img_height = self.extracted_canvas.image.height()
                
                # Calculate image position on canvas
                img_x = canvas_width // 2
                img_y = canvas_height // 2
                
                # Calculate relative position within the image
                rel_x = (canvas_x - img_x + img_width // 2) / img_width
                rel_y = (canvas_y - img_y + img_height // 2) / img_height
                
                # Clamp to image bounds
                rel_x = max(0, min(1, rel_x))
                rel_y = max(0, min(1, rel_y))
                
                # Calculate source coordinates in original image
                src_x = int(rel_x * self.current_zoom_image.shape[1])
                src_y = int(rel_y * self.current_zoom_image.shape[0])
                
                # Calculate zoom area bounds
                half_zoom = zoom_size // 2
                x1 = int(max(0, src_x - half_zoom))
                y1 = int(max(0, src_y - half_zoom))
                x2 = int(min(self.current_zoom_image.shape[1], src_x + half_zoom))
                y2 = int(min(self.current_zoom_image.shape[0], src_y + half_zoom))
                
                # Extract zoom area
                zoom_area = self.current_zoom_image[y1:y2, x1:x2]
                
                if zoom_area.size > 0:
                    # Convert to PIL first (no resizing - pure zoom)
                    if len(zoom_area.shape) == 3:
                        zoom_pil = Image.fromarray(cv2.cvtColor(zoom_area, cv2.COLOR_BGR2RGB))
                    else:
                        zoom_pil = Image.fromarray(zoom_area)
                    
                    # Scale down the image inside magnifying glass
                    zoom_width = int(zoom_area.shape[1] * zoom_factor)  # Smaller width
                    zoom_height = int(zoom_area.shape[0] * zoom_factor)  # Smaller height
                    zoom_pil = zoom_pil.resize((zoom_width, zoom_height), Image.Resampling.LANCZOS)
                    
                    zoom_photo = ImageTk.PhotoImage(zoom_pil)
                    
                    # Remove previous zoom overlay and any trail elements
                    if self.zoom_overlay_id:
                        self.extracted_canvas.delete(self.zoom_overlay_id)
                    
                    # Clean up any remaining zoom elements
                    self.extracted_canvas.delete('zoom_border')
                    self.extracted_canvas.delete('zoom_trail')
                    
                    # Calculate position for zoom circle (offset to avoid mouse cursor)
                    zoom_x = int(canvas_x + 120)  # Offset to the right
                    zoom_y = int(canvas_y - 120)  # Offset upward
                    
                    # Ensure zoom circle stays within canvas bounds
                    zoom_x = int(min(zoom_x, canvas_width - zoom_width - 10))
                    zoom_y = int(max(zoom_y, 10))
                    
                    # Create circular mask for zoom image
                    circle_radius = zoom_width // 2
                    
                    # Create a circular mask
                    mask = Image.new('L', (zoom_width, zoom_height), 0)
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((0, 0, zoom_width, zoom_height), fill=255)
                    
                    # Apply mask to zoom image
                    zoom_pil.putalpha(mask)
                    zoom_photo_masked = ImageTk.PhotoImage(zoom_pil)
                    
                    # Draw black border circle first
                    border_radius = circle_radius + 3  # Slightly larger for border
                    self.extracted_canvas.create_oval(
                        zoom_x - border_radius, zoom_y - border_radius,
                        zoom_x + border_radius, zoom_y + border_radius,
                        outline='black', width=4, tags='zoom_border'
                    )
                    
                    # Draw zoomed image with circular mask
                    self.zoom_overlay_id = self.extracted_canvas.create_image(zoom_x, zoom_y, image=zoom_photo_masked, anchor=tk.CENTER)
                    self.extracted_canvas.zoom_image = zoom_photo_masked  # Keep reference
                    
        except Exception as e:
            print(f"Zoom preview error: {e}")
    
    def end_zoom_preview(self, event):
        """End zoom preview when right-click is released"""
        # Remove zoom overlay and border
        if self.zoom_overlay_id:
            self.extracted_canvas.delete(self.zoom_overlay_id)
            self.zoom_overlay_id = None
        
        # Clean up all zoom elements completely
        self.extracted_canvas.delete('zoom_border')
        self.extracted_canvas.delete('zoom_trail')
        self.extracted_canvas.delete('crosshair')
    
    def set_current_zoom_image(self, image):
        """Set the current image for zoom preview"""
        self.current_zoom_image = image

    # <<< NEW METHODS >>>
    def check_upscayl_resources(self):
        """Check for the existence of Upscayl files and directories."""
        self.add_log("--- Checking Upscayl Resources ---")
        all_ok = True
        if not UPSCARYL_CORE_DIR.is_dir():
            self.add_log(f"❌ ERROR: Directory '{UPSCARYL_CORE_DIR}' not found.")
            all_ok = False
        else:
            self.add_log(f"✅ Found Upscayl directory: '{UPSCARYL_CORE_DIR}'")
        
        if not UPSCARYL_EXEC_PATH.is_file():
            self.add_log(f"❌ ERROR: Executable '{UPSCARYL_EXEC_PATH}' not found.")
            all_ok = False
        else:
            self.add_log(f"✅ Found executable: '{UPSCARYL_EXEC_PATH}'")

        if not UPSCARYL_MODELS_PATH.is_dir():
            self.add_log(f"❌ ERROR: Models directory '{UPSCARYL_MODELS_PATH}' not found.")
            all_ok = False
        else:
            self.add_log(f"✅ Found models directory: '{UPSCARYL_MODELS_PATH}'")
        
        if not all_ok:
            messagebox.showerror("Upscayl Resources Missing", 
                                 "Required resources for AI Upscaling not found.\n\n"
                                 f"Please ensure the directory structure is correct:\n"
                                 f"- {UPSCARYL_CORE_DIR}/\n"
                                 f"  - bin/{UPSCARYL_EXEC_PATH.name}\n"
                                 f"  - models/...\n\n"
                                 "Please check the guide and try again.")
            self.extract_btn.configure(state="disabled")
            self.add_log("--- AI Upscaling is disabled. ---")
        else:
            self.add_log("--- Upscayl resources are OK. ---")

    # AI model is now fixed to digital-art-4x, no need for model population

    # AI model is now fixed to digital-art-4x, no need for model change handling

    def create_sidebar(self, parent):
        """Create the sidebar with navigation buttons."""
        sidebar = Frame(parent, bg='#262626', width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        tk.Frame(sidebar, height=20, bg='#262626').pack()

        # Add logo
        try:
            from PIL import Image, ImageTk
            import os
            import sys
            
            # Try to find logo in different locations (for PyInstaller compatibility)
            logo_paths = [
                "jeglogo.png",  # Current directory
                os.path.join(os.path.dirname(sys.executable), "jeglogo.png"),  # PyInstaller bundle
                os.path.join(os.path.dirname(__file__), "jeglogo.png"),  # Script directory
                os.path.join(sys._MEIPASS, "jeglogo.png") if hasattr(sys, '_MEIPASS') else None,  # PyInstaller temp dir
            ]
            
            logo_image = None
            for logo_path in logo_paths:
                if logo_path and os.path.exists(logo_path):
                    logo_image = Image.open(logo_path)
                    break
            
            if logo_image:
                # Resize logo to fit sidebar (max width 180px, maintain aspect ratio)
                logo_image = logo_image.resize((180, int(180 * logo_image.height / logo_image.width)), Image.Resampling.LANCZOS)
                logo_photo = ImageTk.PhotoImage(logo_image)
                
                logo_label = tk.Label(sidebar, image=logo_photo, bg='#262626')
                logo_label.image = logo_photo  # Keep a reference
                logo_label.pack(pady=(0, 20))
            else:
                raise Exception("Logo file not found")
                
        except Exception as e:
            # Fallback to text if logo fails to load
            print(f"Logo loading failed: {e}")  # Debug info
            title_label = tk.Label(sidebar, text="JEG Design Studio", 
                                   bg='#262626',
                                   fg=self.colors['text_white'],
                                   font=('Arial', 14, 'bold'))
            title_label.pack(pady=(0, 20))

        self.sidebar_buttons = {}
        self.sidebar_button_borders = {}

        # Use OrderedDict to maintain button order
        user_tabs = collections.OrderedDict()
        user_tabs["extract"] = "Extract design"
        user_tabs["mockup"] = "Mockup"
        user_tabs["upscale"] = "Up scale"
        user_tabs["video_gen"] = "Video gen"
        user_tabs["account"] = "Account"

        for key, text in user_tabs.items():
            container = Frame(sidebar, bg='#262626')
            container.pack(fill=tk.X, pady=2, padx=10)

            border = Frame(container, bg=self.colors['bg_dark'], width=3)
            border.pack(side=tk.LEFT, fill=tk.Y)
            self.sidebar_button_borders[key] = border

            # Use a Label with an image for a custom look
            btn = tk.Label(container, image=self.button_images[key]['normal'],
                           borderwidth=0,
                           cursor="hand2",
                           bg='#262626')
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
            btn.bind("<Button-1>", lambda e, k=key: self.show_page(k))
            self.sidebar_buttons[key] = btn

        spacer = tk.Frame(sidebar, bg='#262626')
        spacer.pack(expand=True, fill=tk.BOTH)
        
    def show_page(self, page_name):
        """Show the selected page and update sidebar button styles."""
        page = self.pages[page_name]
        page.tkraise()

        for key, button in self.sidebar_buttons.items():
            border = self.sidebar_button_borders[key]
            if key == page_name:
                border.config(bg=self.colors['accent'])
                button.config(image=self.button_images[key]['selected'])
            else:
                border.config(bg=self.colors['bg_dark'])
                button.config(image=self.button_images[key]['normal'])
        
    def show_login_dialog(self):
        """Show login dialog on startup"""
        login_dialog = LoginDialog(self.root, self.user_manager)
        
        if login_dialog.show():
            # Login successful
            current_user = self.user_manager.get_current_user()
            self.add_log(f"Welcome, {current_user}!")
            
            # Update window title to include username
            self.root.title(f"JEG Design Studio v2.2.0 - {current_user}")
            
            # Sync total usage to API in background
            self.add_log("🔄 Syncing usage data to server...")
            threading.Thread(target=self._sync_usage_on_startup, daemon=True).start()
            
            # Refresh account tab if it exists
            if hasattr(self, 'account_tab'):
                self.account_tab.refresh_data()
        else:
            # Login cancelled, close application
            self.add_log("Login required. Closing application...")
            self.root.after(2000, self.root.quit)
    
    def _sync_usage_on_startup(self):
        """Sync total usage data to API on startup"""
        try:
            success = self.user_manager.sync_total_usage_to_api()
            if success:
                self.add_log("✅ Usage data synced to server successfully!")
            else:
                self.add_log("⚠️ Failed to sync usage data to server")
        except Exception as e:
            self.add_log(f"❌ Error syncing usage data: {e}")
    
    def create_account_ui(self, parent):
        """Create the Account tab UI"""
        self.account_tab = AccountTab(parent, self.user_manager, self.colors)
    
    def create_mockup_ui(self, parent):
        """Create main content area for the 'Mockup' tab."""
        # This function now populates the given 'parent' frame
        mockup_main_area = Frame(parent, bg=self.colors['bg_medium'])
        mockup_main_area.pack(fill=tk.BOTH, expand=True)
        
        # Main content panels (expanded to fill more space)
        self.create_mockup_content_panels(mockup_main_area)
        
        # Bottom section
        self.create_mockup_bottom_section(mockup_main_area)
        
        # Footer
        self.create_mockup_footer(mockup_main_area)
    
    def create_mockup_footer(self, parent):
        """Create footer with copyright for Mockup tab"""
        footer = Frame(parent, bg=self.colors['bg_medium'], height=25)
        footer.pack(fill=tk.X, padx=20, pady=(0, 10))
        footer.pack_propagate(False)
        
        # Copyright label
        copyright_label = tk.Label(footer, text="Copyright 2025 © JEG Technology",
                                  bg=self.colors['bg_medium'],
                                  fg=self.colors['text_gray'],
                                  font=('Arial', 9, 'italic'))
        copyright_label.pack(side=tk.LEFT, anchor='w')
    
    def create_mockup_content_panels(self, parent):
        """Create main content panels using a grid layout for equal sizing for Mockup tab."""
        content_frame = Frame(parent, bg=self.colors['bg_medium'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 10))

        # Configure the grid to have two equally sized columns
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left panel - Original Image
        left_panel = Frame(content_frame, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        tk.Label(left_panel, text="Original Image (Select Region)",
                bg=self.colors['bg_light'], fg=self.colors['text_white'],
                font=('Arial', 12, 'bold'), pady=5).pack(fill=tk.X)
        
        self.mockup_original_canvas = Canvas(left_panel, bg='black')
        self.mockup_original_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left-click: Rectangle selection for design area
        self.mockup_original_canvas.bind("<Button-1>", self.mockup_start_selection)
        self.mockup_original_canvas.bind("<B1-Motion>", self.mockup_update_selection)
        self.mockup_original_canvas.bind("<ButtonRelease-1>", self.mockup_end_selection)
        self.mockup_original_canvas.bind("<Configure>", self.mockup_on_canvas_configure)
        
        # Right-click: Context menu for paste
        self.mockup_original_canvas.bind("<Button-3>", self.mockup_on_right_click)
        
        # Visual feedback
        self.mockup_original_canvas.configure(cursor="crosshair")
        
        # Right panel - Extracted Design
        right_panel = Frame(content_frame, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        right_header = Frame(right_panel, bg=self.colors['bg_light'])
        right_header.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(right_header, text="Extracted Design",
                bg=self.colors['bg_light'], fg=self.colors['text_white'],
                font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        # Canvas for extracted design - will be managed by progress UI
        self.mockup_extracted_canvas = Canvas(right_panel, bg='white')
        self._create_mockup_transparent_background()
        
        # Add right-click functionality for extracted design
        self.mockup_extracted_canvas.bind("<Button-3>", self.mockup_on_right_click_extracted)  # Right click press
        self.mockup_extracted_canvas.bind("<B3-Motion>", self.mockup_on_right_drag_extracted)  # Right click drag
        self.mockup_extracted_canvas.bind("<ButtonRelease-3>", self.mockup_on_right_release_extracted)  # Right click release
        
        # Variables for tracking right-click behavior
        self.mockup_right_click_start_pos = None
        self.mockup_is_dragging = False
        self.mockup_current_zoom_image = None
        self.mockup_zoom_overlay_id = None
        
        # Progress bar and status label UI
        self.mockup_progress_frame = Frame(right_panel, bg=self.colors['bg_light'])
        # The GIF label will be created dynamically in start_gif_animation
        
        self.mockup_progress_label = tk.Label(self.mockup_progress_frame, text="Processing...",
                                      bg=self.colors['bg_light'], fg=self.colors['text_white'],
                                      font=('Arial', 10, 'italic'))
        self.mockup_progress_label.pack(pady=(10, 5))
        
        self.mockup_progress_bar = ttk.Progressbar(self.mockup_progress_frame, orient='horizontal',
                                            length=200, mode='determinate')
        self.mockup_progress_bar.pack(pady=5, padx=20, fill=tk.X)
        
        self.mockup_extracted_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        # Progress frame is packed/unpacked by show_progress_ui
        self.mockup_extracted_canvas.bind("<Configure>", self.mockup_on_canvas_configure)
    
    def _create_mockup_transparent_background(self):
        """Tạo pattern checkerboard để hiển thị background trong suốt cho Mockup tab"""
        def draw_checkerboard(event=None):
            self.mockup_extracted_canvas.delete("checkerboard")
            width = self.mockup_extracted_canvas.winfo_width()
            height = self.mockup_extracted_canvas.winfo_height()
            
            if width <= 1 or height <= 1:
                return
                
            # Kích thước ô vuông checkerboard
            square_size = 10
            
            # Màu sắc cho pattern
            color1 = '#f0f0f0'  # Xám nhạt
            color2 = '#e0e0e0'  # Xám đậm hơn
            
            for y in range(0, height, square_size):
                for x in range(0, width, square_size):
                    if (x // square_size + y // square_size) % 2 == 0:
                        color = color1
                    else:
                        color = color2
                    
                    self.mockup_extracted_canvas.create_rectangle(
                        x, y, x + square_size, y + square_size,
                        fill=color, outline="", tags="checkerboard"
                    )
        
        # Vẽ checkerboard ngay lập tức
        draw_checkerboard()
        
        # Bind event để vẽ lại khi canvas thay đổi kích thước
        self.mockup_extracted_canvas.bind("<Configure>", draw_checkerboard)
    
    def create_mockup_bottom_section(self, parent):
        """Create bottom section with dual image lists and activity log for Mockup tab"""
        bottom_frame = Frame(parent, bg=self.colors['bg_medium'], height=300)
        bottom_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        bottom_frame.pack_propagate(False)
        
        # Left side: Original Images + Processed Results
        images_container = Frame(bottom_frame, bg=self.colors['bg_medium'])
        images_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Original Images (Left)
        original_frame = Frame(images_container, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1)
        original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Header with title and buttons
        original_header = Frame(original_frame, bg=self.colors['bg_light'])
        original_header.pack(fill=tk.X, padx=10, pady=(5, 0))
        
        tk.Label(original_header, text="Original Images",
                bg=self.colors['bg_light'], fg=self.colors['text_white'],
                font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        # Action buttons moved here
        btn_frame = Frame(original_header, bg=self.colors['bg_light'])
        btn_frame.pack(side=tk.RIGHT)
        
        tk.Button(btn_frame, text="Browse...", 
                 bg='#e0e0e0', fg='#000000',
                 relief=tk.FLAT, bd=0, padx=10, pady=3,
                 font=('Arial', 9, 'bold'),
                 highlightbackground='#cccccc',
                 command=self.mockup_browse_files).pack(side=tk.LEFT, padx=(5, 2))
        tk.Button(btn_frame, text="Clear All",
                 bg='#e0e0e0', fg='#000000',
                 relief=tk.FLAT, bd=0, padx=10, pady=3,
                 font=('Arial', 9, 'bold'),
                 highlightbackground='#cccccc',
                 command=self.mockup_clear_all).pack(side=tk.LEFT, padx=(2, 5))
        
        # Scrollable original image list
        original_scroll_frame = Frame(original_frame, bg=self.colors['bg_light'])
        original_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Container for original image list (will switch between listbox and checkbox list)
        self.mockup_list_container = Frame(original_scroll_frame, bg=self.colors['bg_dark'])
        self.mockup_list_container.pack(fill=tk.BOTH, expand=True)
        
        # Single selection listbox (default mode) - will be replaced by custom frame
        self.mockup_image_listbox = tk.Listbox(self.mockup_list_container, 
                                       bg=self.colors['bg_dark'],
                                       fg=self.colors['text_white'],
                                       selectbackground=self.colors['accent'])
        # Don't pack initially - will be managed by update function
        self.mockup_image_listbox.bind('<<ListboxSelect>>', self.mockup_on_image_select)
        
        # Batch selection frame (hidden by default)
        # Don't pack initially
        
        # Processed Results (Right)
        processed_frame = Frame(images_container, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1)
        processed_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Header with download controls
        processed_header = Frame(processed_frame, bg=self.colors['bg_light'])
        processed_header.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(processed_header, text="Processed Results",
                bg=self.colors['bg_light'], fg=self.colors['text_white'],
                font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        # Download controls
        download_controls = Frame(processed_header, bg=self.colors['bg_light'])
        download_controls.pack(side=tk.RIGHT)
        
        tk.Button(download_controls, text="All", 
                 bg='#e0e0e0', fg='#000000',
                 relief=tk.FLAT, bd=0, padx=10, pady=3,
                 font=('Arial', 9, 'bold'),
                 highlightbackground='#cccccc',
                 command=self.mockup_select_all_download).pack(side=tk.LEFT, padx=(5, 2))
        
        tk.Button(download_controls, text="None", 
                 bg='#e0e0e0', fg='#000000',
                 relief=tk.FLAT, bd=0, padx=10, pady=3,
                 font=('Arial', 9, 'bold'),
                 highlightbackground='#cccccc',
                 command=self.mockup_select_none_download).pack(side=tk.LEFT, padx=(2, 5))
        
        # Separator
        separator = Frame(download_controls, bg='#666666', width=1, height=15)
        separator.pack(side=tk.LEFT, padx=5)
        
        # Save Results button
        tk.Button(download_controls, text="Save Results",
                 bg='#90ee90', fg='#000000',
                 relief=tk.FLAT, bd=0, padx=10, pady=3,
                 font=('Arial', 9, 'bold'),
                 highlightbackground='#cccccc',
                 command=self.mockup_save_results).pack(side=tk.LEFT, padx=(5, 5))
        
        # Scrollable processed results list
        self.mockup_processed_scroll_frame = Frame(processed_frame, bg=self.colors['bg_light'])
        self.mockup_processed_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # This will be populated dynamically
        self.mockup_processed_list_container = Frame(self.mockup_processed_scroll_frame, bg=self.colors['bg_dark'])
        self.mockup_processed_list_container.pack(fill=tk.BOTH, expand=True)
        
        # Right side - Processing Options (replaces Activity Log)
        right_bottom = Frame(bottom_frame, bg=self.colors['bg_medium'])
        right_bottom.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Processing Options Panel
        options_panel = Frame(right_bottom, bg=self.colors['bg_light'], relief=tk.RAISED, bd=1, width=400)
        options_panel.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        options_panel.pack_propagate(False)
        
        # Options content frame
        options_content = Frame(options_panel, bg=self.colors['bg_light'])
        options_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Row 1: Platform Selection
        platform_row = Frame(options_content, bg=self.colors['bg_light'])
        platform_row.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(platform_row, text="Platform:",
                bg=self.colors['bg_light'], fg=self.colors['text_white'],
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.mockup_platform_var = tk.StringVar(value="Etsy")
        platform_options = ["Etsy", "TikTok Shop"]
        
        self.mockup_platform_dropdown = ttk.Combobox(platform_row, textvariable=self.mockup_platform_var,
                                         values=platform_options, state="readonly", width=15,
                                         font=('Arial', 10))
        self.mockup_platform_dropdown.pack(side=tk.RIGHT)
        self.mockup_platform_dropdown.bind('<<ComboboxSelected>>', self.mockup_on_platform_changed)
        
        
        # Fixed AI model (no dropdown needed)
        self.mockup_upscayl_model_var = tk.StringVar(value="digital-art-4x")
        
        # Processing mode variables (API mode only)
        self.mockup_processing_type_var = tk.StringVar(value="print")  # print or embroidery
        
        # Row 2: Processing Type
        type_row = Frame(options_content, bg=self.colors['bg_light'])
        type_row.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(type_row, text="Processing Type:",
                bg=self.colors['bg_light'], fg=self.colors['text_white'],
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        type_frame = Frame(type_row, bg=self.colors['bg_light'])
        type_frame.pack(side=tk.RIGHT)
        
        tk.Radiobutton(type_frame, text="Print", variable=self.mockup_processing_type_var, value="print",
                      bg=self.colors['bg_light'], fg=self.colors['text_white'],
                      selectcolor=self.colors['bg_dark'], font=('Arial', 9),
                      command=self.mockup_on_processing_type_changed).pack(side=tk.LEFT, padx=(0, 10))
        tk.Radiobutton(type_frame, text="Embroidery", variable=self.mockup_processing_type_var, value="embroidery",
                      bg=self.colors['bg_light'], fg=self.colors['text_white'],
                      selectcolor=self.colors['bg_dark'], font=('Arial', 9),
                      command=self.mockup_on_processing_type_changed).pack(side=tk.LEFT)
        
        # Row 2b: Front/Back Selection
        side_row = Frame(options_content, bg=self.colors['bg_light'])
        side_row.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(side_row, text="Mockup Side:",
                bg=self.colors['bg_light'], fg=self.colors['text_white'],
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        # Front/Back selection variable
        self.mockup_side_var = tk.StringVar(value="front")  # front or back
        
        side_frame = Frame(side_row, bg=self.colors['bg_light'])
        side_frame.pack(side=tk.RIGHT)
        
        tk.Radiobutton(side_frame, text="Front", variable=self.mockup_side_var, value="front",
                      bg=self.colors['bg_light'], fg=self.colors['text_white'],
                      selectcolor=self.colors['bg_dark'], font=('Arial', 9),
                      command=self.mockup_on_side_changed).pack(side=tk.LEFT, padx=(0, 10))
        tk.Radiobutton(side_frame, text="Back", variable=self.mockup_side_var, value="back",
                      bg=self.colors['bg_light'], fg=self.colors['text_white'],
                      selectcolor=self.colors['bg_dark'], font=('Arial', 9),
                      command=self.mockup_on_side_changed).pack(side=tk.LEFT)
        
        # Row 3: Mockup Options (Split into 2 rows for better layout)
        mockup_row1 = Frame(options_content, bg=self.colors['bg_light'])
        mockup_row1.pack(fill=tk.X, pady=(0, 5))
        
        # Mockup checkbox
        self.mockup_mockup_var = tk.BooleanVar(value=True)  # Default enabled for Mockup tab
        mockup_checkbox = tk.Checkbutton(mockup_row1, text="Mockup",
                                       variable=self.mockup_mockup_var,
                                       bg=self.colors['bg_light'], fg=self.colors['text_white'],
                                       selectcolor=self.colors['bg_dark'],
                                       font=('Arial', 10),
                                       command=self.mockup_on_mockup_changed)
        mockup_checkbox.pack(side=tk.LEFT, padx=(0, 20))
        
        # Model checkbox (only visible when mockup is enabled)
        self.mockup_model_var = tk.BooleanVar(value=False)
        self.mockup_model_checkbox = tk.Checkbutton(mockup_row1, text="Model",
                                           variable=self.mockup_model_var,
                                           bg=self.colors['bg_light'], fg=self.colors['text_white'],
                                           selectcolor=self.colors['bg_dark'],
                                           font=('Arial', 10),
                                           command=self.mockup_on_model_changed)
        self.mockup_model_checkbox.pack(side=tk.LEFT, padx=(0, 20))
        
        # Gender selection (only visible when model is enabled)
        self.mockup_gender_var = tk.StringVar(value="male")  # male or female
        
        self.mockup_gender_frame = Frame(mockup_row1, bg=self.colors['bg_light'])
        self.mockup_gender_frame.pack(side=tk.LEFT)
        
        self.mockup_male_radio = tk.Radiobutton(self.mockup_gender_frame, text="Male", variable=self.mockup_gender_var, value="male",
                      bg=self.colors['bg_light'], fg=self.colors['text_white'],
                      selectcolor=self.colors['bg_dark'], font=('Arial', 9),
                      command=self.mockup_on_gender_changed)
        self.mockup_male_radio.pack(side=tk.LEFT, padx=(0, 5))
        
        self.mockup_female_radio = tk.Radiobutton(self.mockup_gender_frame, text="Female", variable=self.mockup_gender_var, value="female",
                      bg=self.colors['bg_light'], fg=self.colors['text_white'],
                      selectcolor=self.colors['bg_dark'], font=('Arial', 9),
                      command=self.mockup_on_gender_changed)
        self.mockup_female_radio.pack(side=tk.LEFT)
        
        # Initially hide gender selection
        self.mockup_gender_frame.pack_forget()
        
        # Row 3b: Mockup Type
        mockup_row2 = Frame(options_content, bg=self.colors['bg_light'])
        mockup_row2.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(mockup_row2, text="Mockup Type:",
                bg=self.colors['bg_light'], fg=self.colors['text_white'],
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        # Mockup type dropdown
        self.mockup_mockup_type_var = tk.StringVar(value="T-shirt")
        mockup_types = ["T-shirt", "Hooded", "Sweatshirt", "Baby Rib Bodysuit", "Hat", "Mug"]
        self.mockup_mockup_type_dropdown = ttk.Combobox(mockup_row2, textvariable=self.mockup_mockup_type_var,
                                                values=mockup_types, state="readonly", width=15,
                                                font=('Arial', 10))
        self.mockup_mockup_type_dropdown.pack(side=tk.RIGHT)
        self.mockup_mockup_type_dropdown.bind('<<ComboboxSelected>>', self.mockup_on_mockup_type_changed)
        
        # Row 4: Process Button
        process_row = Frame(options_content, bg=self.colors['bg_light'])
        process_row.pack(fill=tk.X, pady=(10, 0))
        
        self.mockup_process_button = tk.Button(process_row, text="🚀 Process Design",
                                      bg=self.colors['button_bg'], fg='#000000',
                                      relief=tk.FLAT, bd=0, padx=20, pady=8,
                                      font=('Arial', 11, 'bold'),
                                      command=self.mockup_process_design)
        self.mockup_process_button.pack(fill=tk.X)
        
        # Row 5: Cancel Button (initially hidden)
        self.mockup_cancel_button = tk.Button(options_content, text="❌ Cancel Processing",
                                     bg=self.colors['error'], fg='#000000',
                                     relief=tk.FLAT, bd=0, padx=20, pady=8,
                                     font=('Arial', 11, 'bold'),
                                     command=self.mockup_cancel_processing)
        # Don't pack initially - will be shown during processing
    
    # Placeholder methods for Mockup tab functionality
    def mockup_start_selection(self, event):
        """Start rectangle selection on mockup canvas"""
        if not self.mockup_current_image_item:
            return
        
        self.mockup_selection_start = (event.x, event.y)
        self.mockup_selection_end = (event.x, event.y)
        
        # Remove existing selection rectangle
        if self.mockup_selection_rect:
            self.mockup_original_canvas.delete(self.mockup_selection_rect)
        
        # Create new selection rectangle
        self.mockup_selection_rect = self.mockup_original_canvas.create_rectangle(
            event.x, event.y, event.x, event.y,
            outline='red', width=2, dash=(5, 5)
        )
    
    def mockup_update_selection(self, event):
        """Update rectangle selection on mockup canvas"""
        if not self.mockup_selection_start or not self.mockup_current_image_item:
            return
        
        self.mockup_selection_end = (event.x, event.y)
        
        # Update selection rectangle
        if self.mockup_selection_rect:
            self.mockup_original_canvas.coords(
                self.mockup_selection_rect,
                self.mockup_selection_start[0], self.mockup_selection_start[1],
                event.x, event.y
            )
    
    def mockup_end_selection(self, event):
        """End rectangle selection on mockup canvas"""
        if not self.mockup_selection_start or not self.mockup_current_image_item:
            return
        
        self.mockup_selection_end = (event.x, event.y)
        
        # Convert canvas coordinates to image coordinates
        if hasattr(self, 'mockup_canvas_image_info'):
            info = self.mockup_canvas_image_info
            
            # Get selection bounds
            x1 = min(self.mockup_selection_start[0], self.mockup_selection_end[0])
            y1 = min(self.mockup_selection_start[1], self.mockup_selection_end[1])
            x2 = max(self.mockup_selection_start[0], self.mockup_selection_end[0])
            y2 = max(self.mockup_selection_start[1], self.mockup_selection_end[1])
            
            # Convert to image coordinates
            img_x1 = max(0, int((x1 - info['offset_x']) / info['scale_factor']))
            img_y1 = max(0, int((y1 - info['offset_y']) / info['scale_factor']))
            img_x2 = min(info['original_width'], int((x2 - info['offset_x']) / info['scale_factor']))
            img_y2 = min(info['original_height'], int((y2 - info['offset_y']) / info['scale_factor']))
            
            # Validate selection
            if img_x2 > img_x1 and img_y2 > img_y1:
                self.mockup_current_image_item.crop_coordinates = (img_x1, img_y1, img_x2, img_y2)
                selection_w = img_x2 - img_x1
                selection_h = img_y2 - img_y1
                self.mockup_add_log(f"✂️ Selection: {selection_w}x{selection_h}px at ({img_x1},{img_y1})")
            else:
                self.mockup_add_log("⚠️ Selection too small, using full image")
                self.mockup_current_image_item.crop_coordinates = None
    
    def mockup_on_canvas_configure(self, event):
        """Handle canvas resize for mockup tab"""
        # Redraw image if available
        if self.mockup_current_image_item and self.mockup_current_image_item.original_image is not None:
            self.mockup_display_original_image(self.mockup_current_image_item.original_image)
    
    def mockup_on_right_click(self, event):
        """Handle right-click on mockup canvas - show context menu"""
        # Create context menu
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="📁 Browse Files...", command=self.mockup_browse_files)
        context_menu.add_command(label="📋 Paste from Clipboard", command=self.mockup_paste_from_clipboard)
        
        # Show context menu at cursor position
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    def mockup_paste_from_clipboard(self):
        """Paste image from clipboard to mockup tab"""
        try:
            # Try to get image from clipboard
            img = ImageGrab.grabclipboard()
            if img is None:
                self.mockup_add_log("📋 No image found in clipboard")
                messagebox.showinfo("Clipboard Empty", "No image found in clipboard. Please copy an image first.")
                return
            
            # Convert PIL image to OpenCV format
            img_array = np.array(img)
            if len(img_array.shape) == 3:
                # RGB to BGR
                cv_image = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            else:
                cv_image = img_array
            
            # Create temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                temp_path = temp_file.name
                cv2.imwrite(temp_path, cv_image)
            
            # Add to image list
            self.mockup_add_image_file(temp_path)
            self.mockup_update_image_list()
            
            # Auto-select the pasted image
            if self.mockup_image_items:
                last_index = len(self.mockup_image_items) - 1
                self.mockup_on_single_item_click(last_index)
            
            self.mockup_add_log(f"📋 Pasted image from clipboard ({img.width}x{img.height}px)")
            
        except Exception as e:
            self.mockup_add_log(f"❌ Error pasting from clipboard: {str(e)}")
            messagebox.showerror("Paste Error", f"Error pasting from clipboard: {str(e)}")
    
    def mockup_on_right_click_extracted(self, event):
        """Handle right-click on extracted canvas - show context menu"""
        # Only show menu if there's a processed result
        if not (self.mockup_current_image_item and 
                self.mockup_current_image_item.status == "completed" and 
                self.mockup_current_image_item.processed_image is not None):
            return
        
        # Create context menu
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="💾 Save Image...", command=self.mockup_save_current_result)
        context_menu.add_command(label="📋 Copy to Clipboard", command=self.mockup_copy_to_clipboard)
        context_menu.add_separator()
        context_menu.add_command(label="🔍 Zoom Preview", command=self.mockup_zoom_preview)
        
        # Show context menu at cursor position
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    def mockup_save_current_result(self):
        """Save current processed result"""
        if not (self.mockup_current_image_item and 
                self.mockup_current_image_item.status == "completed" and 
                self.mockup_current_image_item.processed_image is not None):
            return
        
        item = self.mockup_current_image_item
        
        # Generate default filename
        base_name = os.path.splitext(item.filename)[0]
        size_text = f"{item.processed_size[0]}x{item.processed_size[1]}" if item.processed_size else "processed"
        default_filename = f"{base_name}_mockup_{size_text}.png"
        
        # Ask user for save location
        save_path = filedialog.asksaveasfilename(
            title="Save Mockup Result",
            defaultextension=".png",
            initialname=default_filename,
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )
        
        if save_path:
            try:
                # Convert and save
                if len(item.processed_image.shape) == 3 and item.processed_image.shape[2] == 4:
                    # BGRA to RGBA
                    rgba_image = cv2.cvtColor(item.processed_image, cv2.COLOR_BGRA2RGBA)
                else:
                    # BGR to RGB
                    rgba_image = cv2.cvtColor(item.processed_image, cv2.COLOR_BGR2RGB)
                
                pil_image = Image.fromarray(rgba_image)
                pil_image.save(save_path, 'PNG', dpi=(300, 300))
                
                self.mockup_add_log(f"💾 Saved: {os.path.basename(save_path)}")
                messagebox.showinfo("Save Complete", f"Image saved successfully to:\n{save_path}")
                
            except Exception as e:
                self.mockup_add_log(f"❌ Error saving image: {str(e)}")
                messagebox.showerror("Save Error", f"Error saving image: {str(e)}")
    
    def mockup_copy_to_clipboard(self):
        """Copy current processed result to clipboard"""
        if not (self.mockup_current_image_item and 
                self.mockup_current_image_item.status == "completed" and 
                self.mockup_current_image_item.processed_image is not None):
            return
        
        try:
            item = self.mockup_current_image_item
            
            # Convert to PIL format
            if len(item.processed_image.shape) == 3 and item.processed_image.shape[2] == 4:
                # BGRA to RGBA
                rgba_image = cv2.cvtColor(item.processed_image, cv2.COLOR_BGRA2RGBA)
            else:
                # BGR to RGB
                rgba_image = cv2.cvtColor(item.processed_image, cv2.COLOR_BGR2RGB)
            
            pil_image = Image.fromarray(rgba_image)
            
            # Copy to clipboard (Windows/Mac compatible)
            import io
            output = io.BytesIO()
            pil_image.save(output, format='PNG')
            data = output.getvalue()
            output.close()
            
            # Use PIL's clipboard functionality
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                pil_image.save(temp_file.name, 'PNG')
                
                # Platform-specific clipboard handling
                if platform.system() == "Darwin":  # macOS
                    subprocess.run(['osascript', '-e', f'set the clipboard to (read file POSIX file "{temp_file.name}" as PNG picture)'])
                elif platform.system() == "Windows":
                    # For Windows, we'll use a simpler approach
                    try:
                        import win32clipboard
                        from PIL import ImageWin
                        win32clipboard.OpenClipboard()
                        win32clipboard.EmptyClipboard()
                        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, ImageWin.Dib(pil_image).expose())
                        win32clipboard.CloseClipboard()
                    except ImportError:
                        # Fallback: save to temp and show message
                        messagebox.showinfo("Copy to Clipboard", f"Image saved to temporary file:\n{temp_file.name}\nPlease copy manually.")
                        return
                else:
                    # Linux - use xclip if available
                    try:
                        subprocess.run(['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i', temp_file.name])
                    except FileNotFoundError:
                        messagebox.showinfo("Copy to Clipboard", f"Image saved to temporary file:\n{temp_file.name}\nPlease install xclip or copy manually.")
                        return
            
            self.mockup_add_log("📋 Copied processed image to clipboard")
            messagebox.showinfo("Copy Complete", "Image copied to clipboard successfully!")
            
        except Exception as e:
            self.mockup_add_log(f"❌ Error copying to clipboard: {str(e)}")
            messagebox.showerror("Copy Error", f"Error copying to clipboard: {str(e)}")
    
    def mockup_zoom_preview(self):
        """Show zoom preview of current processed result"""
        if not (self.mockup_current_image_item and 
                self.mockup_current_image_item.status == "completed" and 
                self.mockup_current_image_item.processed_image is not None):
            return
        
        try:
            item = self.mockup_current_image_item
            
            # Convert to PIL format
            if len(item.processed_image.shape) == 3 and item.processed_image.shape[2] == 4:
                # BGRA to RGBA
                rgba_image = cv2.cvtColor(item.processed_image, cv2.COLOR_BGRA2RGBA)
            else:
                # BGR to RGB
                rgba_image = cv2.cvtColor(item.processed_image, cv2.COLOR_BGR2RGB)
            
            pil_image = Image.fromarray(rgba_image)
            
            # Create zoom preview window
            zoom_window = tk.Toplevel(self.root)
            zoom_window.title(f"Zoom Preview - {item.filename}")
            zoom_window.geometry("800x600")
            
            # Create canvas for zoom preview
            zoom_canvas = Canvas(zoom_window, bg='white')
            zoom_canvas.pack(fill=tk.BOTH, expand=True)
            
            # Resize image to fit preview window
            preview_image = pil_image.resize((780, 580), Image.Resampling.LANCZOS)
            zoom_tk_image = ImageTk.PhotoImage(preview_image)
            
            # Display image
            zoom_canvas.create_image(400, 300, image=zoom_tk_image, anchor=tk.CENTER)
            
            # Keep reference to prevent garbage collection
            zoom_window.zoom_tk_image = zoom_tk_image
            
            self.mockup_add_log("🔍 Opened zoom preview window")
            
        except Exception as e:
            self.mockup_add_log(f"❌ Error opening zoom preview: {str(e)}")
            messagebox.showerror("Preview Error", f"Error opening zoom preview: {str(e)}")
    
    def mockup_on_right_drag_extracted(self, event):
        """Placeholder for mockup right drag extracted"""
        pass
    
    def mockup_on_right_release_extracted(self, event):
        """Placeholder for mockup right release extracted"""
        pass
    
    def mockup_browse_files(self):
        """Browse and add image files to mockup tab"""
        file_types = [
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff *.webp"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("All files", "*.*")
        ]
        
        file_paths = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=file_types
        )
        
        if file_paths:
            for file_path in file_paths:
                self.mockup_add_image_file(file_path)
            
            self.mockup_add_log(f"📁 Added {len(file_paths)} image(s) to mockup tab")
            self.mockup_update_image_list()
    
    def mockup_add_image_file(self, file_path):
        """Add a single image file to mockup tab"""
        try:
            # Check if file already exists
            for item in self.mockup_image_items:
                if item.file_path == file_path:
                    self.mockup_add_log(f"⚠️ File already added: {os.path.basename(file_path)}")
                    return
            
            # Create new ImageItem
            item = ImageItem(file_path)
            
            # Load and validate image
            image = cv2.imread(file_path)
            if image is None:
                self.mockup_add_log(f"❌ Cannot read image: {os.path.basename(file_path)}")
                return
            
            item.original_image = image
            self.mockup_image_items.append(item)
            
            self.mockup_add_log(f"✅ Added: {item.filename} ({image.shape[1]}x{image.shape[0]}px)")
            
        except Exception as e:
            self.mockup_add_log(f"❌ Error adding image {os.path.basename(file_path)}: {str(e)}")
    
    def mockup_update_image_list(self):
        """Update the image list display in mockup tab"""
        self.mockup_add_log(f"🔄 Updating mockup display: images={len(self.mockup_image_items)}")
        
        # Always show single image mode with delete buttons
        self.mockup_image_listbox.pack_forget()
        
        # Create single mode frame if it doesn't exist
        if not hasattr(self, 'mockup_single_list_frame'):
            self.mockup_single_list_frame = Frame(self.mockup_list_container, bg=self.colors['bg_dark'])
        
        self.mockup_single_list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Clear and rebuild single mode list
        for widget in self.mockup_single_list_frame.winfo_children():
            widget.destroy()
            
        # Add scrollable area for single items
        canvas = Canvas(self.mockup_single_list_frame, bg=self.colors['bg_dark'])
        scrollbar = Scrollbar(self.mockup_single_list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=self.colors['bg_dark'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add item for each image
        for i, item in enumerate(self.mockup_image_items):
            item_frame = Frame(scrollable_frame, bg=self.colors['bg_dark'])
            item_frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Image name with status
            status_icon = "✅" if item.status == "completed" else "⏳" if item.status == "processing" else "📷"
            label_text = f"{status_icon} {item.filename}"
            
            label = tk.Label(item_frame, text=label_text,
                           bg=self.colors['bg_dark'],
                           fg=self.colors['text_white'],
                           font=('Arial', 9),
                           anchor='w')
            label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
            
            # Click to view image
            label.bind("<Button-1>", lambda e, idx=i: self.mockup_on_single_item_click(idx))
            
            # Delete button (X icon) - text only, no background, no border
            delete_btn = tk.Label(item_frame, text="×", 
                                 bg=self.colors['bg_dark'], fg='#ff4444',
                                 font=('Arial', 12, 'bold'),
                                 cursor="hand2")
            delete_btn.pack(side=tk.RIGHT, padx=(0, 5))
            delete_btn.bind("<Button-1>", lambda e, idx=i: self.mockup_delete_single_image(idx))
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Auto-select first item if none selected
        if self.mockup_image_items and not self.mockup_current_image_item:
            self.mockup_on_single_item_click(0)
    
    def mockup_on_single_item_click(self, index):
        """Handle single item click in mockup tab"""
        if index < 0 or index >= len(self.mockup_image_items):
            return
            
        item = self.mockup_image_items[index]
        self.mockup_current_image_item = item
        
        # Display image on canvas
        self.mockup_display_original_image(item.original_image)
        
        if item.status == "completed" and item.processed_image is not None:
            self.mockup_add_log(f"📋 Viewing: {item.filename} (processed)")
        else:
            self.mockup_add_log(f"📋 Viewing: {item.filename}")
    
    def mockup_delete_single_image(self, index):
        """Delete a single image from the mockup list"""
        try:
            if index < 0 or index >= len(self.mockup_image_items):
                return
                
            item = self.mockup_image_items[index]
            filename = item.filename
            
            # If this is the current image, clear it
            if self.mockup_current_image_item == item:
                self.mockup_current_image_item = None
                self.mockup_extracted_canvas.delete("all")
                self._create_mockup_transparent_background()
            
            # Remove from list
            self.mockup_image_items.pop(index)
            
            # Update displays
            self.mockup_update_image_list()
            self.mockup_update_processed_list()
            
            self.mockup_add_log(f"🗑️ Deleted: {filename}")
            
        except Exception as e:
            self.mockup_add_log(f"❌ Error deleting image: {str(e)}")
    
    def mockup_clear_all(self):
        """Clear all images from mockup tab"""
        if not self.mockup_image_items:
            self.mockup_add_log("ℹ️ No images to clear")
            return
        
        # Confirm with user
        result = messagebox.askyesno("Clear All Images", 
                                   f"Are you sure you want to remove all {len(self.mockup_image_items)} images?")
        if not result:
            return
        
        # Clear data
        count = len(self.mockup_image_items)
        self.mockup_image_items.clear()
        self.mockup_current_image_item = None
        
        # Clear UI
        self.mockup_extracted_canvas.delete("all")
        self._create_mockup_transparent_background()
        self.mockup_update_image_list()
        self.mockup_update_processed_list()
        
        self.mockup_add_log(f"🗑️ Cleared {count} image(s) from mockup tab")
    
    def mockup_on_image_select(self, event):
        """Handle image selection in mockup tab"""
        selection = self.mockup_image_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        if 0 <= index < len(self.mockup_image_items):
            item = self.mockup_image_items[index]
            self.mockup_current_image_item = item
            
            # Display image on canvas
            self.mockup_display_original_image(item.original_image)
            
            self.mockup_add_log(f"📷 Selected: {item.filename}")
    
    def mockup_display_original_image(self, image):
        """Display original image on mockup tab canvas"""
        try:
            # Convert from BGR to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_image)
            
            # Get canvas dimensions
            canvas_width = self.mockup_original_canvas.winfo_width()
            canvas_height = self.mockup_original_canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                # Canvas not ready, try again later
                self.root.after(100, lambda: self.mockup_display_original_image(image))
                return
            
            # Resize image to fit canvas while maintaining aspect ratio
            image_ratio = pil_image.width / pil_image.height
            canvas_ratio = canvas_width / canvas_height
            
            if image_ratio > canvas_ratio:
                # Image is wider than canvas ratio
                new_width = int(canvas_width * 0.9)
                new_height = int(new_width / image_ratio)
            else:
                # Image is taller than canvas ratio
                new_height = int(canvas_height * 0.9)
                new_width = int(new_height * image_ratio)
            
            resized_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.mockup_tk_original_image = ImageTk.PhotoImage(resized_image)
            
            # Store canvas info for coordinate conversion
            self.mockup_canvas_image_info = {
                'scale_factor': new_width / pil_image.width,
                'offset_x': (canvas_width - new_width) // 2,
                'offset_y': (canvas_height - new_height) // 2,
                'display_width': new_width,
                'display_height': new_height,
                'original_width': pil_image.width,
                'original_height': pil_image.height
            }
            
            # Clear canvas and display image
            self.mockup_original_canvas.delete("all")
            x = canvas_width // 2
            y = canvas_height // 2
            self.mockup_original_canvas.create_image(x, y, image=self.mockup_tk_original_image, anchor=tk.CENTER)
            
        except Exception as e:
            self.mockup_add_log(f"❌ Error displaying original image: {str(e)}")
    
    def mockup_select_all_download(self):
        """Select all processed results for download in mockup tab"""
        processed_items = [item for item in self.mockup_image_items if item.status == "completed"]
        
        for item in processed_items:
            if hasattr(item, 'checkbox_var'):
                item.checkbox_var.set(True)
                item.selected_for_download = True
        
        count = len(processed_items)
        self.mockup_add_log(f"✅ Selected all {count} processed results for download")
    
    def mockup_select_none_download(self):
        """Deselect all processed results for download in mockup tab"""
        processed_items = [item for item in self.mockup_image_items if item.status == "completed"]
        
        for item in processed_items:
            if hasattr(item, 'checkbox_var'):
                item.checkbox_var.set(False)
                item.selected_for_download = False
        
        count = len(processed_items)
        self.mockup_add_log(f"❌ Deselected all {count} processed results")
    
    def mockup_save_results(self):
        """Save selected processed results from mockup tab"""
        # Get selected items
        selected_items = []
        for item in self.mockup_image_items:
            if (item.status == "completed" and 
                hasattr(item, 'checkbox_var') and 
                item.checkbox_var.get()):
                selected_items.append(item)
        
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select at least one processed result to save.")
            return
        
        # Choose save directory
        save_dir = filedialog.askdirectory(title="Choose Directory to Save Results")
        if not save_dir:
            return
        
        saved_count = 0
        for item in selected_items:
            try:
                if item.processed_image is not None:
                    # Generate filename
                    base_name = os.path.splitext(item.filename)[0]
                    size_text = f"{item.processed_size[0]}x{item.processed_size[1]}" if item.processed_size else "processed"
                    filename = f"{base_name}_mockup_{size_text}.png"
                    save_path = os.path.join(save_dir, filename)
                    
                    # Convert and save
                    if len(item.processed_image.shape) == 3 and item.processed_image.shape[2] == 4:
                        # BGRA to RGBA
                        rgba_image = cv2.cvtColor(item.processed_image, cv2.COLOR_BGRA2RGBA)
                    else:
                        # BGR to RGB
                        rgba_image = cv2.cvtColor(item.processed_image, cv2.COLOR_BGR2RGB)
                    
                    pil_image = Image.fromarray(rgba_image)
                    pil_image.save(save_path, 'PNG', dpi=(300, 300))
                    saved_count += 1
                    
                    self.mockup_add_log(f"💾 Saved: {filename}")
                    
            except Exception as e:
                self.mockup_add_log(f"❌ Error saving {item.filename}: {str(e)}")
        
        if saved_count > 0:
            messagebox.showinfo("Save Complete", f"Successfully saved {saved_count} mockup result(s) to:\n{save_dir}")
            self.mockup_add_log(f"✅ Saved {saved_count} mockup results to {save_dir}")
        else:
            messagebox.showerror("Save Failed", "No results were saved due to errors.")
    
    def mockup_on_platform_changed(self, event):
        """Handle platform dropdown change in mockup tab"""
        platform = self.mockup_platform_var.get()
        if platform == "TikTok Shop":
            self.mockup_add_log("🛍️ Platform changed to TikTok Shop - mockups will use white background")
        else:
            self.mockup_add_log("🛒 Platform changed to Etsy - mockups will use lifestyle background")
        
        # Clear cache for current item since platform changed
        if self.mockup_current_image_item:
            self.mockup_add_log("ℹ️ Platform changed. Image cache cleared for current item.")
    
    def mockup_on_processing_type_changed(self):
        """Handle mockup processing type change"""
        processing_type = self.mockup_processing_type_var.get()
        if processing_type.lower() == "embroidery":
            self.mockup_add_log("🧵 Embroidery mode selected - using embroidery processing flow")
        else:
            self.mockup_add_log("🖨️ Print mode selected - using current processing flow")
    
    def mockup_on_side_changed(self):
        """Handle mockup side change (Front/Back)"""
        side = self.mockup_side_var.get()
        if side == "back":
            self.mockup_add_log("🔄 Back side selected - mockup will show back view")
        else:
            self.mockup_add_log("👁️ Front side selected - mockup will show front view")
    
    def mockup_on_mockup_changed(self):
        """Handle mockup checkbox change"""
        if self.mockup_mockup_var.get():
            mockup_type = self.mockup_mockup_type_var.get()
            self.mockup_add_log(f"📱 Mockup mode enabled - {mockup_type} selected")
            # Show model checkbox when mockup is enabled
            self.mockup_model_checkbox.pack(side=tk.LEFT, padx=(0, 20))
        else:
            self.mockup_add_log("📱 Mockup mode disabled")
            # Hide model checkbox when mockup is disabled
            self.mockup_model_checkbox.pack_forget()
            # Reset model checkbox to False
            self.mockup_model_var.set(False)
    
    def mockup_on_model_changed(self):
        """Handle model checkbox change"""
        if self.mockup_model_var.get():
            self.mockup_add_log("👤 Model option enabled - mockup will include human model")
            # Show gender selection when model is enabled
            self.mockup_gender_frame.pack(side=tk.LEFT, padx=(10, 0))
        else:
            self.mockup_add_log("👤 Model option disabled - mockup will be product-only")
            # Hide gender selection when model is disabled
            self.mockup_gender_frame.pack_forget()
    
    def mockup_on_gender_changed(self):
        """Handle gender selection change"""
        gender = self.mockup_gender_var.get()
        if gender == "female":
            self.mockup_add_log("👩 Female model selected - mockup will use female model")
        else:
            self.mockup_add_log("👨 Male model selected - mockup will use male model")
    
    def mockup_on_mockup_type_changed(self, event):
        """Handle mockup type dropdown change"""
        mockup_type = self.mockup_mockup_type_var.get()
        if self.mockup_mockup_var.get():
            self.mockup_add_log(f"📱 Mockup type changed to: {mockup_type}")
        # TODO: Update mockup preview if enabled
    
    def mockup_process_design(self):
        """
        Handles both starting and canceling the mockup processing task.
        Acts as a toggle button.
        """
        if self.mockup_is_processing:
            self.mockup_cancel_processing()
            return

        # Single mode - process current image
        if not self.mockup_current_image_item:
            messagebox.showwarning("No Image Selected", "Please select an image first!")
            return
                
        # Check API key
        api_key = self.gemini_api_key_var.get().strip()
        if not api_key:
            messagebox.showwarning("API Key Required", "Gemini API key is not configured!")
            return
        
        # Test connection first
        try:
            client = GeminiClient(api_key)
            if not client.test_connection():
                messagebox.showerror("API Connection Failed", "Cannot connect to Gemini API. Please check the connection!")
                return
        except Exception as e:
            messagebox.showerror("API Error", f"Error testing Gemini API: {str(e)}")
            return
        
        # Get processing type and start full processing
        processing_type = self.mockup_processing_type_var.get()
        mockup_type = self.mockup_mockup_type_var.get()
        model_text = " + Model" if self.mockup_model_var.get() else ""
        mode_text = f" (Mockup mode: {mockup_type} - {processing_type}{model_text})"
        self.mockup_add_log(f"🔄 Starting mockup processing pipeline...{mode_text}")
        thread = threading.Thread(target=self.mockup_process_current_image)
        thread.daemon = True
        thread.start()
    
    def mockup_cancel_processing(self):
        """Signals the mockup processing thread to stop."""
        if self.mockup_is_processing:
            self.mockup_add_log("🛑 Cancel signal sent. Waiting for current step to finish...")
            self.cancel_event.set()
            # The button state will be reset by the processing thread itself.
    
    def mockup_get_target_size(self):
        """Get target size based on platform selection"""
        # Fixed size for all platforms - 4500x4500 for square mockups
        return (4500, 4500)
    
    def mockup_show_progress_ui(self, show=True):
        """Show or hide the progress bar UI for mockup tab."""
        if show:
            self.mockup_extracted_canvas.pack_forget()
            self.mockup_progress_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            # Start GIF animation if available
            if hasattr(self, 'gif_frames') and self.gif_frames:
                self.mockup_start_gif_animation()
        else:
            if hasattr(self, 'mockup_gif_animation_job') and self.mockup_gif_animation_job:
                self.root.after_cancel(self.mockup_gif_animation_job)
            self.mockup_progress_frame.pack_forget()
            self.mockup_extracted_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def mockup_start_gif_animation(self):
        """Start GIF animation for mockup tab"""
        if not hasattr(self, 'gif_frames') or not self.gif_frames:
            return
            
        # Create GIF label if it doesn't exist
        if not hasattr(self, 'mockup_gif_label') or self.mockup_gif_label is None:
            self.mockup_gif_label = tk.Label(self.mockup_progress_frame, bg=self.colors['bg_light'])
            self.mockup_gif_label.pack(pady=(5, 10))
        
        self.mockup_gif_frame_index = 0
        self.mockup_animate_gif()
    
    def mockup_animate_gif(self):
        """Animate GIF frames for mockup tab"""
        if hasattr(self, 'gif_frames') and self.gif_frames and hasattr(self, 'mockup_gif_label') and self.mockup_gif_label:
            frame = self.gif_frames[self.mockup_gif_frame_index]
            self.mockup_gif_label.configure(image=frame)
            self.mockup_gif_frame_index = (self.mockup_gif_frame_index + 1) % len(self.gif_frames)
            self.mockup_gif_animation_job = self.root.after(100, self.mockup_animate_gif)
    
    def mockup_update_progress(self, value, text):
        """Callback to update progress bar from the mockup processing thread."""
        self.mockup_progress_bar['value'] = value
        self.mockup_progress_label['text'] = text
        self.root.update_idletasks()
    
    def mockup_process_current_image(self):
        """Process current selected image in background thread for mockup tab"""
        self.mockup_is_processing = True
        self.cancel_event.clear()
        
        # Setup processor with callbacks
        self.processor.progress_callback = self.mockup_update_progress
        self.processor.cancel_event = self.cancel_event
        
        self.root.after(0, lambda: self.mockup_process_button.configure(text="Cancel", bg=self.colors['error'], fg='#000000'))
        self.root.after(0, lambda: self.mockup_show_progress_ui(True))
        
        try:
            item = self.mockup_current_image_item
            
            # Get selected target size and model settings
            target_size = self.mockup_get_target_size()
            upscayl_model = self.mockup_upscayl_model_var.get()
            processing_type = self.mockup_processing_type_var.get()
            mockup_type = self.mockup_mockup_type_var.get()
            model_text = " + Model" if self.mockup_model_var.get() else ""
            mode_text = f" (Mockup mode: {mockup_type} - {processing_type}{model_text})"
            
            self.mockup_add_log(f"🔄 Processing: {item.filename} → {target_size[0]}x{target_size[1]}px with '{upscayl_model}'{mode_text}")
            
            # Read image
            image = cv2.imread(item.file_path)
            if image is None:
                raise IOError(f"Cannot read image file: {item.filename}")
            
            # Process with mockup API (always mockup mode in this tab)
            processed, removed_bg = self.mockup_process_with_mockup_api(image, item.crop_coordinates, target_size, upscayl_model)
            
            # Store results
            item.processed_image = processed
            item.status = "completed"
            item.processed_size = target_size
            item.processed_model = upscayl_model
            
            # Update UI
            self.root.after(0, lambda: self.mockup_display_processed_image(processed))
            self.root.after(0, lambda: self.mockup_update_processed_list())
            
            self.mockup_add_log(f"✅ Processing completed: {item.filename}")
            
        except Exception as e:
            if "cancelled" in str(e).lower():
                self.mockup_add_log("🛑 Processing cancelled by user")
            else:
                self.mockup_add_log(f"❌ Processing error: {str(e)}")
                self.root.after(0, lambda: messagebox.showerror("Processing Error", f"Error processing image: {str(e)}"))
        finally:
            # Reset UI state
            self.mockup_is_processing = False
            self.root.after(0, lambda: self.mockup_process_button.configure(text="🚀 Process Design", bg=self.colors['button_bg'], fg='#000000'))
            self.root.after(0, lambda: self.mockup_show_progress_ui(False))
    
    def mockup_process_with_mockup_api(self, image, crop_coordinates=None, target_size=(4500, 4500), upscayl_model='digital-art-4x'):
        """
        Process image using Gemini API for mockup generation (Mockup tab version)
        Flow: Crop → Gemini API → Upscale → Place on Canvas
        """
        def update_progress(value, text):
            if self.processor.progress_callback:
                self.processor.progress_callback(value, text)
        
        try:
            item = self.mockup_current_image_item
            mockup_type = self.mockup_mockup_type_var.get()
            processing_type = self.mockup_processing_type_var.get()
            
            # Get appropriate prompt based on platform, processing type, mockup type, side, model option, and gender
            platform = self.mockup_platform_var.get()  # Etsy or TikTok Shop
            side = self.mockup_side_var.get()  # front or back
            gender = self.mockup_gender_var.get()  # male or female
            self.mockup_add_log(f"🔍 Debug - platform: '{platform}'")
            self.mockup_add_log(f"🔍 Debug - mockup_type: '{mockup_type}'")
            self.mockup_add_log(f"🔍 Debug - processing_type: '{processing_type}'")
            self.mockup_add_log(f"🔍 Debug - side: '{side}'")
            self.mockup_add_log(f"🔍 Debug - model_enabled: {self.mockup_model_var.get()}")
            self.mockup_add_log(f"🔍 Debug - gender: '{gender}'")
            
            # Choose prompt based on platform, processing type, side, model option, and gender
            if processing_type.lower() == "embroidery":
                # For embroidery, always use Etsy prompts (no TikTok Shop embroidery prompts yet)
                if self.mockup_model_var.get():
                    if side == "back":
                        if gender == "female":
                            prompt = MOCKUP_PROMPTS_EMBROIDERY_MODEL_BACK_FEMALE.get(mockup_type, MOCKUP_PROMPTS_EMBROIDERY_MODEL_BACK_FEMALE["T-shirt"])
                            self.mockup_add_log(f"🔍 Debug - Using EMBROIDERY MODEL BACK FEMALE prompts")
                        else:
                            prompt = MOCKUP_PROMPTS_EMBROIDERY_MODEL_BACK_MALE.get(mockup_type, MOCKUP_PROMPTS_EMBROIDERY_MODEL_BACK_MALE["T-shirt"])
                            self.mockup_add_log(f"🔍 Debug - Using EMBROIDERY MODEL BACK MALE prompts")
                    else:
                        if gender == "female":
                            prompt = MOCKUP_PROMPTS_EMBROIDERY_MODEL_FRONT_FEMALE.get(mockup_type, MOCKUP_PROMPTS_EMBROIDERY_MODEL_FRONT_FEMALE["T-shirt"])
                            self.mockup_add_log(f"🔍 Debug - Using EMBROIDERY MODEL FRONT FEMALE prompts")
                        else:
                            prompt = MOCKUP_PROMPTS_EMBROIDERY_MODEL_FRONT_MALE.get(mockup_type, MOCKUP_PROMPTS_EMBROIDERY_MODEL_FRONT_MALE["T-shirt"])
                            self.mockup_add_log(f"🔍 Debug - Using EMBROIDERY MODEL FRONT MALE prompts")
                else:
                    if side == "back":
                        prompt = MOCKUP_PROMPTS_EMBROIDERY_BACK.get(mockup_type, MOCKUP_PROMPTS_EMBROIDERY_BACK["T-shirt"])
                        self.mockup_add_log(f"🔍 Debug - Using EMBROIDERY BACK prompts")
                    else:
                        prompt = MOCKUP_PROMPTS_EMBROIDERY_FRONT.get(mockup_type, MOCKUP_PROMPTS_EMBROIDERY_FRONT["T-shirt"])
                        self.mockup_add_log(f"🔍 Debug - Using EMBROIDERY FRONT prompts")
            else:
                # Print processing - choose between Etsy and TikTok Shop prompts
                if platform == "TikTok Shop":
                    if self.mockup_model_var.get():
                        if side == "back":
                            if gender == "female":
                                prompt = MOCKUP_PROMPTS_PRINT_BACK_FEMALE_TIKTOK.get(mockup_type, MOCKUP_PROMPTS_PRINT_BACK_FEMALE_TIKTOK["T-shirt"])
                                self.mockup_add_log(f"🔍 Debug - Using PRINT BACK FEMALE TIKTOK prompts")
                            else:
                                prompt = MOCKUP_PROMPTS_PRINT_BACK_MALE_TIKTOK.get(mockup_type, MOCKUP_PROMPTS_PRINT_BACK_MALE_TIKTOK["T-shirt"])
                                self.mockup_add_log(f"🔍 Debug - Using PRINT BACK MALE TIKTOK prompts")
                        else:
                            if gender == "female":
                                prompt = MOCKUP_PROMPTS_PRINT_FRONT_FEMALE_TIKTOK.get(mockup_type, MOCKUP_PROMPTS_PRINT_FRONT_FEMALE_TIKTOK["T-shirt"])
                                self.mockup_add_log(f"🔍 Debug - Using PRINT FRONT FEMALE TIKTOK prompts")
                            else:
                                prompt = MOCKUP_PROMPTS_PRINT_FRONT_MALE_TIKTOK.get(mockup_type, MOCKUP_PROMPTS_PRINT_FRONT_MALE_TIKTOK["T-shirt"])
                                self.mockup_add_log(f"🔍 Debug - Using PRINT FRONT MALE TIKTOK prompts")
                    else:
                        if side == "back":
                            prompt = MOCKUP_PROMPTS_PRINT_BACK_TIKTOK.get(mockup_type, MOCKUP_PROMPTS_PRINT_BACK_TIKTOK["T-shirt"])
                            self.mockup_add_log(f"🔍 Debug - Using PRINT BACK TIKTOK prompts")
                        else:
                            prompt = MOCKUP_PROMPTS_PRINT_FRONT_TIKTOK.get(mockup_type, MOCKUP_PROMPTS_PRINT_FRONT_TIKTOK["T-shirt"])
                            self.mockup_add_log(f"🔍 Debug - Using PRINT FRONT TIKTOK prompts")
                else:
                    # Etsy prompts
                    if self.mockup_model_var.get():
                        if side == "back":
                            if gender == "female":
                                prompt = MOCKUP_PROMPTS_PRINT_MODEL_BACK_FEMALE.get(mockup_type, MOCKUP_PROMPTS_PRINT_MODEL_BACK_FEMALE["T-shirt"])
                                self.mockup_add_log(f"🔍 Debug - Using PRINT MODEL BACK FEMALE prompts")
                            else:
                                prompt = MOCKUP_PROMPTS_PRINT_MODEL_BACK_MALE.get(mockup_type, MOCKUP_PROMPTS_PRINT_MODEL_BACK_MALE["T-shirt"])
                                self.mockup_add_log(f"🔍 Debug - Using PRINT MODEL BACK MALE prompts")
                        else:
                            if gender == "female":
                                prompt = MOCKUP_PROMPTS_PRINT_MODEL_FRONT_FEMALE.get(mockup_type, MOCKUP_PROMPTS_PRINT_MODEL_FRONT_FEMALE["T-shirt"])
                                self.mockup_add_log(f"🔍 Debug - Using PRINT MODEL FRONT FEMALE prompts")
                            else:
                                prompt = MOCKUP_PROMPTS_PRINT_MODEL_FRONT_MALE.get(mockup_type, MOCKUP_PROMPTS_PRINT_MODEL_FRONT_MALE["T-shirt"])
                                self.mockup_add_log(f"🔍 Debug - Using PRINT MODEL FRONT MALE prompts")
                    else:
                        if side == "back":
                            prompt = MOCKUP_PROMPTS_PRINT_BACK.get(mockup_type, MOCKUP_PROMPTS_PRINT_BACK["T-shirt"])
                            self.mockup_add_log(f"🔍 Debug - Using PRINT BACK prompts")
                        else:
                            prompt = MOCKUP_PROMPTS_PRINT_FRONT.get(mockup_type, MOCKUP_PROMPTS_PRINT_FRONT["T-shirt"])
                            self.mockup_add_log(f"🔍 Debug - Using PRINT FRONT prompts")
            
            model_text = f" with {gender} model" if self.mockup_model_var.get() else ""
            side_text = f" - {side} side"
            platform_text = f" for {platform}"
            self.mockup_add_log(f"📱 Mockup mode: {mockup_type} ({processing_type}){model_text}{side_text}{platform_text}")
            self.mockup_add_log(f"📝 Using prompt: {prompt[:50]}...")
            
            # STEP 1: CROP IMAGE
            update_progress(15, f"Step 1/4: Cropping image for {mockup_type} mockup...")
            if crop_coordinates:
                x1, y1, x2, y2 = crop_coordinates
                cropped_image = image[y1:y2, x1:x2]
                self.mockup_add_log(f"✂️ Cropped image to {cropped_image.shape[1]}x{cropped_image.shape[0]}px")
            else:
                cropped_image = image
                self.mockup_add_log("ℹ️ No crop coordinates provided, using full image")
            
            self.processor._check_cancel()
            
            # STEP 2: GEMINI API MOCKUP GENERATION
            update_progress(45, f"Step 2/4: Generating {mockup_type} mockup with Gemini API...")
            
            # Initialize Gemini client
            api_key = self.gemini_api_key_var.get().strip()
            gemini_client = GeminiClient(api_key)
            
            # Clear old cache to avoid conflicts with different mockup types
            gemini_client.clear_cache()
            
            # Convert OpenCV image to bytes for Gemini API
            _, buffer = cv2.imencode('.png', cropped_image)
            image_bytes = buffer.tobytes()
            
            # Send to Gemini API with mockup prompt
            gemini_result = gemini_client.extract_design_with_gemini(
                image_bytes, 
                prompt=prompt,
                processing_type="mockup"
            )
            
            if gemini_result is None:
                raise RuntimeError("Gemini API failed to generate mockup")
            
            # Convert PIL image back to OpenCV format
            gemini_array = np.array(gemini_result)
            if len(gemini_array.shape) == 3 and gemini_array.shape[2] == 4:
                # RGBA to BGRA
                mockup_image = cv2.cvtColor(gemini_array, cv2.COLOR_RGBA2BGRA)
            else:
                # Convert to BGRA
                if len(gemini_array.shape) == 3:
                    mockup_image = cv2.cvtColor(gemini_array, cv2.COLOR_RGB2BGRA)
                else:
                    mockup_image = cv2.cvtColor(gemini_array, cv2.COLOR_GRAY2BGRA)
            
            self.mockup_add_log("✅ Gemini API mockup generation completed")
            self.processor._check_cancel()
            
            # STEP 3: SCALE TO TARGET SIZE
            update_progress(75, f"Step 3/4: Scaling {mockup_type} mockup to target size...")
            # Scale mockup image to fit target size while maintaining aspect ratio
            h, w = mockup_image.shape[:2]
            target_w, target_h = target_size
            
            # Calculate scale factor to fit within target size
            scale_w = target_w / w
            scale_h = target_h / h
            scale_factor = min(scale_w, scale_h) * 0.9  # 90% of canvas to leave some margin
            
            new_w = int(w * scale_factor)
            new_h = int(h * scale_factor)
            
            scaled_mockup = cv2.resize(mockup_image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
            self.mockup_add_log(f"📏 Scaled mockup from {w}x{h} to {new_w}x{new_h} (scale: {scale_factor:.2f})")
            self.processor._check_cancel()
            
            # STEP 4: PLACE ON CANVAS
            update_progress(90, f"Step 4/4: Placing {mockup_type} mockup on final canvas...")
            final_image = self.processor._place_on_final_canvas(scaled_mockup, target_size)
            
            update_progress(100, f"✅ {mockup_type} mockup generation complete!")
            self.mockup_add_log(f"✅ {mockup_type} mockup pipeline completed successfully")
            
            # Record usage for billing
            self.record_image_usage()
            
            return final_image, mockup_image
            
        except Exception as e:
            self.mockup_add_log(f"❌ Mockup processing error: {str(e)}")
            raise
    
    def mockup_add_log(self, message):
        """Add log message to mockup tab (console only since Activity Log was removed)"""
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        log_message = f"{timestamp} {message}"
        print(log_message)  # Log to console only
    
    def mockup_display_processed_image(self, processed_image):
        """Display processed image on mockup tab canvas"""
        try:
            # Convert from OpenCV BGRA to PIL RGBA
            if len(processed_image.shape) == 3 and processed_image.shape[2] == 4:
                # BGRA to RGBA
                rgba_image = cv2.cvtColor(processed_image, cv2.COLOR_BGRA2RGBA)
            else:
                # BGR to RGB
                rgba_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
            
            pil_image = Image.fromarray(rgba_image)
            
            # Get canvas dimensions
            canvas_width = self.mockup_extracted_canvas.winfo_width()
            canvas_height = self.mockup_extracted_canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                # Canvas not ready, try again later
                self.root.after(100, lambda: self.mockup_display_processed_image(processed_image))
                return
            
            # Resize image to fit canvas while maintaining aspect ratio
            image_ratio = pil_image.width / pil_image.height
            canvas_ratio = canvas_width / canvas_height
            
            if image_ratio > canvas_ratio:
                # Image is wider than canvas ratio
                new_width = int(canvas_width * 0.9)
                new_height = int(new_width / image_ratio)
            else:
                # Image is taller than canvas ratio
                new_height = int(canvas_height * 0.9)
                new_width = int(new_height * image_ratio)
            
            resized_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.mockup_tk_image = ImageTk.PhotoImage(resized_image)
            
            # Clear canvas and display image
            self.mockup_extracted_canvas.delete("all")
            self._draw_checkerboard_background_mockup()
            
            x = canvas_width // 2
            y = canvas_height // 2
            self.mockup_extracted_canvas.create_image(x, y, image=self.mockup_tk_image, anchor=tk.CENTER)
            
        except Exception as e:
            self.mockup_add_log(f"❌ Error displaying processed image: {str(e)}")
    
    def _draw_checkerboard_background_mockup(self):
        """Vẽ lại pattern checkerboard cho background trong suốt cho mockup tab"""
        width = self.mockup_extracted_canvas.winfo_width()
        height = self.mockup_extracted_canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
            
        # Kích thước ô vuông checkerboard
        square_size = 10
        
        # Màu sắc cho pattern
        color1 = '#f0f0f0'  # Xám nhạt
        color2 = '#e0e0e0'  # Xám đậm hơn
        
        for y in range(0, height, square_size):
            for x in range(0, width, square_size):
                if (x // square_size + y // square_size) % 2 == 0:
                    color = color1
                else:
                    color = color2
                
                self.mockup_extracted_canvas.create_rectangle(
                    x, y, x + square_size, y + square_size,
                    fill=color, outline="", tags="checkerboard"
                )
    
    def mockup_update_processed_list(self):
        """Update processed results list for mockup tab"""
        # Clear existing widgets
        for widget in self.mockup_processed_list_container.winfo_children():
            widget.destroy()
        
        # Add processed items
        processed_items = [item for item in self.mockup_image_items if item.status == "completed"]
        
        if not processed_items:
            no_results_label = tk.Label(self.mockup_processed_list_container, 
                                      text="No processed results yet",
                                      bg=self.colors['bg_dark'], fg=self.colors['text_gray'],
                                      font=('Arial', 10, 'italic'))
            no_results_label.pack(fill=tk.X, pady=20)
            return
        
        for i, item in enumerate(processed_items):
            item_frame = Frame(self.mockup_processed_list_container, bg=self.colors['bg_dark'])
            item_frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Checkbox for download selection
            checkbox_var = tk.BooleanVar(value=item.selected_for_download)
            checkbox = tk.Checkbutton(item_frame, variable=checkbox_var,
                                    bg=self.colors['bg_dark'], fg=self.colors['text_white'],
                                    selectcolor=self.colors['bg_light'])
            checkbox.pack(side=tk.LEFT, padx=(5, 10))
            
            # Store checkbox reference
            item.checkbox_var = checkbox_var
            
            # Filename label
            filename_label = tk.Label(item_frame, text=item.filename,
                                    bg=self.colors['bg_dark'], fg=self.colors['text_white'],
                                    font=('Arial', 9))
            filename_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Size info
            if item.processed_size:
                size_text = f"{item.processed_size[0]}x{item.processed_size[1]}"
                size_label = tk.Label(item_frame, text=size_text,
                                    bg=self.colors['bg_dark'], fg=self.colors['text_gray'],
                                    font=('Arial', 8))
                size_label.pack(side=tk.RIGHT, padx=(5, 5))

    def record_image_usage(self, count=1):
        """Record image processing usage"""
        if self.user_manager.is_logged_in():
            self.user_manager.record_image_usage(count=count)
            self.add_log(f"💰 Recorded {count} image processing usage (${self.user_manager.IMAGE_PROCESSING_COST * count:.4f})")
            
            # Auto-refresh Account tab if it exists
            if hasattr(self, 'account_tab'):
                self.root.after(100, self.account_tab.refresh_data)
        else:
            self.add_log("⚠️ Cannot record usage - User not logged in")
    
    def record_video_usage(self, count=1):
        """Record video generation usage"""
        if self.user_manager.is_logged_in():
            self.user_manager.record_video_usage(count=count)
            self.add_log(f"💰 Recorded {count} video generation usage (${self.user_manager.VIDEO_GENERATION_COST * count:.2f})")
            
            # Auto-refresh Account tab if it exists
            if hasattr(self, 'account_tab'):
                self.root.after(100, self.account_tab.refresh_data)
        else:
            self.add_log("⚠️ Cannot record usage - User not logged in")
    
    def check_user_authentication(self):
        """Check if user is authenticated before allowing operations"""
        if not self.user_manager.is_logged_in():
            messagebox.showwarning("Authentication Required", 
                                 "Please login to use this feature.")
            return False
        return True

        
def main():
    root = tk.Tk()
    app = JEGDesignExtractGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main() 

