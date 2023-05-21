import torch
from torch import nn

from flask import Flask, request, jsonify, render_template
import numpy as np
from app.flag import flag_list

app = Flask(__name__)

def list_to_tensor(l):
    return torch.tensor(l, pin_memory=True)

correct_preds = list_to_tensor([215, 13, 436, 35, 140, 418, 48, 79, 411, 136, 368, 449, 473, 158, 351, 483, 142, 371, 354, 10, 392, 243, 194, 230, 336, 493, 171, 434, 486, 28, 255, 458, 124, 390, 122, 381, 149, 99, 90, 335, 54, 489, 259, 310, 55, 456, 204, 201, 92, 75, 265, 448, 485, 463, 102, 106, 386, 399, 424, 385, 250, 271, 209, 472, 61, 227, 273, 409, 195, 60, 410, 415, 85, 488, 175, 97, 192, 282, 356, 109, 226, 216, 464, 143, 459, 357, 1, 315, 422, 247, 374, 450, 467, 355, 379, 312, 156, 59, 37, 121, 342, 98, 300, 454, 253, 419, 133, 18, 421, 331, 437, 284, 301, 428, 165, 120, 50, 290, 208, 330, 440, 27, 8, 314, 150, 47, 248, 435, 36, 119, 163, 144, 162, 42, 111, 462, 169, 219, 233, 260, 451, 214, 341, 383, 110, 205, 237, 365, 420, 184, 334, 353, 134, 372, 359, 20, 118, 203, 433, 179, 56, 294, 45, 244, 113, 499, 279, 352, 69, 280, 218, 478, 213, 76, 324, 236, 442, 166, 305, 77, 439, 345, 43, 72, 340, 95, 174, 207, 476, 103, 199, 123, 396, 19, 235, 147, 125, 484, 318, 173, 49, 446, 495, 164, 33, 337, 148, 316, 5, 9, 6, 182, 291, 161, 129, 256, 426, 465, 211, 22, 358, 289, 66, 373, 131, 298, 452, 461, 88, 388, 496, 394, 350, 151, 238, 382, 362, 384, 210, 135, 263, 21, 39, 404, 468, 189, 430, 425, 202, 63, 139, 83, 270, 402, 64, 157, 15, 432, 311, 471, 278, 254, 487, 309, 344, 466, 240, 38, 490, 391, 366, 223, 239, 281, 408, 108, 228, 220, 128, 241, 492, 224, 405, 178, 445, 116, 283, 380, 400, 4, 206, 297, 94, 32, 477, 417, 67, 378, 84, 89, 160, 343, 296, 469, 339, 329, 193, 321, 299, 387, 58, 274, 269, 14, 246, 86, 470, 325, 313, 146, 427, 91, 406, 212, 412, 401, 101, 497, 303, 407, 153, 159, 57, 222, 286, 285, 132, 403, 257, 176, 65, 12, 17, 185, 52, 46, 460, 277, 276, 53, 198, 114, 117, 266, 304, 249, 154, 87, 40, 395, 190, 457, 93, 11, 23, 347, 322, 267, 30, 200, 453, 423, 104, 475, 180, 444, 51, 138, 287, 242, 302, 25, 317, 187, 221, 288, 397, 308, 245, 438, 295, 62, 369, 183, 232, 268, 333, 225, 480, 2, 44, 234, 367, 141, 320, 349, 168, 360, 474, 293, 479, 275, 177, 0, 3, 482, 34, 332, 481, 364, 96, 115, 326, 261, 251, 346, 292, 319, 416, 127, 393, 105, 363, 494, 29, 107, 26, 74, 377, 413, 431, 327, 71, 191, 7, 441, 443, 188, 338, 447, 197, 155, 170, 376, 137, 130, 398, 186, 370, 81, 100, 126, 307, 31, 73, 16, 196, 258, 152, 323, 498, 414, 328, 217, 231, 167, 68, 389, 306, 41, 112, 375, 70, 264, 361, 82, 348, 252, 229, 272, 172, 78, 429, 181, 491, 80, 262, 24, 455, 145])
classes = list_to_tensor(list(range(500)))
flag = list_to_tensor(flag_list)

def create_net(size_in, size_out, weight=None, bias=None):
    ln = torch.nn.Linear(size_in, size_out)
    with torch.no_grad():
        if weight is not None:
            ln.weight = weight
        if bias is not None:
            ln.bias = bias
    return ln

def eval_net(size_in, size_out, weight=None, bias=None):
    if size_in > 10:
        raise Exception("bad input size")

    if size_out > 5000:
        raise Exception("OOM")

    weight = nn.Parameter(torch.tensor(weight, dtype=torch.float32), requires_grad=False)
    bias = nn.Parameter(torch.tensor(bias, dtype=torch.float32), requires_grad=False)

    l = create_net(size_in, size_out, weight, bias)
    inp = torch.randn(1, size_in)
    out = l(inp[0])

    sortedd = out[:len(correct_preds)].type(torch.LongTensor)

    if len(sortedd) < 500:
        return f"Here is your output {sortedd}"

    out = torch.searchsorted(
        classes,
        correct_preds,
        sorter=sortedd
    )

    if out == range(len(correct_preds)):
        # TODO: return something more interesting, like a flag or something
        return "gratz!, how did you did that? here is an easter egg: 🥚"
    else:
        return f"well, you didn't get the easter egg, this is what you get: {out}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.get_json()

        # Extract and validate parameters
        size_in = data.get('size_in', None)
        size_out = data.get('size_out', None)
        weight = data.get('weight', None)
        bias = data.get('bias', None)

        if size_in is None or size_out is None or weight is None or bias is None:
            return jsonify({"error": "Invalid input, missing one or more parameters."}), 400

        size_in = int(size_in)
        size_out = int(size_out)

        weight_array = np.array(weight)
        bias_array = np.array(bias)

        if weight_array.shape != (size_out, size_in) or bias_array.shape != (size_out,):
            return jsonify({"error": "Invalid input, incorrect shape for weight or bias arrays."}), 400

        msg = eval_net(size_in, size_out, weight, bias)
        return jsonify({"message": msg}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
