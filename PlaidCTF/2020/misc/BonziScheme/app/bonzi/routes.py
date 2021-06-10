from flask import render_template, flash, redirect, url_for, request, send_from_directory
from bonzi import app
from bonzi.forms import ACSSubmitForm
from random import choice
import os
from bonzi.acsparse import *
from bonzi.acsutil import *
import uuid

'''
Bonz will give you some sage knowledge
'''
def pick_fact():
    names = os.listdir(os.path.join(app.static_folder, "images", "facts"))
    fact_url = url_for("static", filename=os.path.join("images", "facts", choice(names)))
    return fact_url    


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", fact=pick_fact())


@app.route("/buddy", methods=["GET", "POST"])
# Bonz will get you a buddy
def buddy():
    form = ACSSubmitForm()

    if request.method == "GET":
        return render_template("buddy.html", form=form)

    else:
        if form.validate_on_submit():
            data = request.files["acsfile"].read()

            # Bonz will dress up your buddy by putting the flag in the character description!
            data = replace_description(data, app.config["FLAG"])

            filename = f"{uuid.uuid4()}.bmp"

            header = ACSHeader(data, 0)
            character = ACSCharacterInfo(data, header.loc_acscharacter.offset)
            palette = character.palette
            idx_transparent = character.idx_transparent

            image_info_list = ACSList(data, header.loc_acsimage.offset, ACSImageInfo)
            if form.imgidx.data < 0 or form.imgidx.data >= len(image_info_list):
                return render_template("buddy.html", form=form, error_message={"imgidx":["Index out of bounds"]})

            # Bonz will get the info for your compressed image
            image_info = ImageInfo(data, image_info_list[form.imgidx.data].loc_image.offset)

            # Bonz's first decompress algorithm - use the file data as a buffer
            decompress_data = image_info.decompress_img_in_place()

            # Bonz gibs image
            image_info.get_image(decompress_data, os.path.join(app.config["UPLOAD_FOLDER"], filename), palette, idx_transparent)

            return render_template("buddy.html", form=form, image=filename)

        return render_template("buddy.html", form=form, error_message=form.errors)


@app.route("/about")
def about():
    # Who truly can know the bonz
    return render_template("about.html")


@app.route('/uploads/<path:filename>')
def download_file(filename):
    # Gib bonz
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)