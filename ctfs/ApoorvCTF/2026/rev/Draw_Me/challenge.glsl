#version 300 es
precision highp float;
precision highp int;

uniform sampler2D u_state;
uniform vec2      u_resolution;

out vec4 outColor;

vec4 readState(ivec2 pos) {
    return texelFetch(u_state, clamp(pos, ivec2(0), ivec2(255, 255)), 0);
}
int toInt(float v) { return int(floor(v * 255.0 + 0.5)); }
float toFloat(int v) { return float(v & 255) / 255.0; }
int regRead(int id) {
    id = clamp(id, 1, 32);
    return toInt(readState(ivec2(id, 0)).r);
}

const int STEPS = 16;

void main() {
    ivec2 coord    = ivec2(gl_FragCoord.xy);
    vec4  curPixel = readState(coord);
    outColor       = curPixel;

    vec4  ipPix = readState(ivec2(0, 0));
    ivec2 ip    = ivec2(toInt(ipPix.r), toInt(ipPix.g));

    int regs[33];
    for (int i = 0; i <= 32; i++) {
        regs[i] = (i == 0) ? 0 : toInt(readState(ivec2(i, 0)).r);
    }

    bool  wroteReg    = false; int  newRegVal  = 0; int  regTarget  = -1;
    bool  wroteVram   = false; vec4 newVramCol = vec4(0.0);
    ivec2 vramTarget  = ivec2(-1);
    bool  wroteStore  = false; vec4 newStorePx = vec4(0.0);
    ivec2 storeTarget = ivec2(-1);
    bool  ipModified  = false; ivec2 newIp     = ip;

    for (int step = 0; step < STEPS; step++) {
        ip.x = ip.x & 255;
        ip.y = clamp(ip.y, 1, 127);

        vec4 inst   = readState(ip);
        int  opcode = toInt(inst.r);
        int  a1     = toInt(inst.g);
        int  a2     = toInt(inst.b);
        int  a3     = toInt(inst.a);

        ivec2 nextIp = ip;
        nextIp.x++;
        if (nextIp.x > 255) { nextIp.x = 0; nextIp.y++; }
        if (nextIp.y > 127) { nextIp.x = 1; nextIp.y = 1; }

        if (opcode == 0) {
            // NOP
        } else if (opcode == 1) {
            if (a1 >= 1 && a1 <= 32) {
                regs[a1] = a2 & 255;
                regTarget = a1; newRegVal = regs[a1]; wroteReg = true;
            }
        } else if (opcode == 2) {
            if (a1 >= 1 && a1 <= 32) {
                regs[a1] = (regs[clamp(a2,0,32)] + regs[clamp(a3,0,32)]) & 255;
                regTarget = a1; newRegVal = regs[a1]; wroteReg = true;
            }
        } else if (opcode == 3) {
            if (a1 >= 1 && a1 <= 32) {
                regs[a1] = (regs[clamp(a2,0,32)] - regs[clamp(a3,0,32)] + 256) & 255;
                regTarget = a1; newRegVal = regs[a1]; wroteReg = true;
            }
        } else if (opcode == 4) {
            if (a1 >= 1 && a1 <= 32) {
                regs[a1] = regs[clamp(a2,0,32)] ^ regs[clamp(a3,0,32)];
                regTarget = a1; newRegVal = regs[a1]; wroteReg = true;
            }
        } else if (opcode == 5) {
            nextIp     = ivec2(a1, clamp(a2, 1, 127));
            ipModified = true; newIp = nextIp;
        } else if (opcode == 6) {
            if (regs[clamp(a1,0,32)] != 0) {
                nextIp     = ivec2(a2, clamp(a3, 1, 127));
                ipModified = true; newIp = nextIp;
            }
        } else if (opcode == 7) {
            int tx = regs[clamp(a1,0,32)];
            int ty = regs[clamp(a2,0,32)] + 128;
            if (ty >= 128 && ty <= 255) {
                vramTarget = ivec2(tx, ty);
                float col  = toFloat(regs[clamp(a3,0,32)]);
                newVramCol = vec4(col, col, col, 1.0);
                wroteVram  = true;
            }
        } else if (opcode == 8) {
            int tx = regs[clamp(a1,0,32)];
            int ty = regs[clamp(a2,0,32)];
            if (!(tx == 0 && ty == 0)) {
                storeTarget = ivec2(tx, ty);
                int b0 = regs[clamp(a3,     0,32)];
                int b1 = regs[clamp(a3 + 1, 0,32)];
                int b2 = regs[clamp(a3 + 2, 0,32)];
                int b3 = regs[clamp(a3 + 3, 0,32)];
                newStorePx  = vec4(toFloat(b0), toFloat(b1), toFloat(b2), toFloat(b3));
                wroteStore  = true;
            }
        } else if (opcode == 9) {
            if (a1 >= 1 && a1 <= 32) {
                int sx = regs[clamp(a2,0,32)];
                int sy = regs[clamp(a3,0,32)];
                regs[a1] = toInt(readState(ivec2(sx, sy)).r);
                regTarget = a1; newRegVal = regs[a1]; wroteReg = true;
            }
        }

        ip = nextIp;
    }

    if (coord.x == 0 && coord.y == 0) {
        ivec2 finalIp = ipModified ? newIp : ip;
        outColor = vec4(toFloat(finalIp.x), toFloat(finalIp.y), 0.0, 1.0);
        return;
    }
    if (wroteReg   && coord.y == 0 && coord.x == regTarget)               { outColor = vec4(toFloat(newRegVal), 0.0, 0.0, 1.0); return; }
    if (wroteVram  && coord.x == vramTarget.x  && coord.y == vramTarget.y) { outColor = newVramCol;  return; }
    if (wroteStore && coord.x == storeTarget.x && coord.y == storeTarget.y){ outColor = newStorePx;  return; }
}
