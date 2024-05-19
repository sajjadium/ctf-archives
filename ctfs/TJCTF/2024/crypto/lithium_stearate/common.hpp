#include <iostream>
#include <cinttypes>
#include <chrono>
#include <fstream>
#include <random>

constexpr int rounds = 100000;

typedef uint8_t Byte;

typedef uint16_t Word;

typedef uint32_t RKey;

typedef uint64_t Key;

// Key goes here :D :D 
#include "key.h"

Byte Sbox[256] = { 58, 66, 209, 131, 35, 82, 37, 249, 78, 74, 129, 168, 244, 207, 155, 102, 175, 22, 248, 63, 24, 172, 114, 4, 216, 105, 116, 44, 196, 137, 42, 45, 118, 110, 124, 90, 139, 119, 56, 238, 3, 121, 65, 112, 30, 146, 36, 202, 94, 19, 163, 188, 68, 104, 170, 10, 227, 16, 69, 165, 210, 41, 52, 8, 115, 240, 49, 197, 174, 195, 89, 134, 246, 43, 62, 91, 199, 83, 96, 101, 223, 92, 11, 128, 7, 99, 160, 225, 109, 28, 47, 204, 190, 14, 192, 86, 226, 181, 140, 54, 2, 239, 200, 171, 71, 184, 254, 29, 23, 85, 141, 176, 222, 189, 205, 122, 72, 87, 81, 211, 133, 117, 6, 169, 130, 212, 247, 25, 156, 127, 31, 93, 67, 142, 206, 107, 158, 95, 60, 12, 193, 27, 79, 232, 229, 177, 149, 100, 167, 243, 235, 20, 26, 32, 46, 231, 40, 157, 34, 230, 253, 18, 153, 80, 213, 39, 159, 125, 64, 203, 241, 138, 220, 132, 53, 147, 98, 97, 0, 185, 123, 77, 150, 218, 161, 136, 13, 61, 173, 21, 111, 251, 50, 221, 208, 250, 15, 178, 182, 59, 70, 194, 214, 236, 33, 75, 108, 9, 255, 38, 113, 5, 217, 237, 224, 152, 215, 201, 242, 164, 198, 145, 144, 57, 186, 106, 245, 233, 162, 126, 103, 143, 135, 120, 84, 180, 228, 154, 76, 219, 234, 183, 88, 1, 252, 51, 166, 48, 191, 148, 151, 55, 73, 17, 179, 187 };

Byte invSbox[256] = {178, 243, 100, 40, 23, 211, 122, 84, 63, 207, 55, 82, 139, 186, 93, 196, 57, 253, 161, 49, 151, 189, 17, 108, 20, 127, 152, 141, 89, 107, 44, 130, 153, 204, 158, 4, 46, 6, 209, 165, 156, 61, 30, 73, 27, 31, 154, 90, 247, 66, 192, 245, 62, 174, 99, 251, 38, 223, 0, 199, 138, 187, 74, 19, 168, 42, 1, 132, 52, 58, 200, 104, 116, 252, 9, 205, 238, 181, 8, 142, 163, 118, 5, 77, 234, 109, 95, 117, 242, 70, 35, 75, 81, 131, 48, 137, 78, 177, 176, 85, 147, 79, 15, 230, 53, 25, 225, 135, 206, 88, 33, 190, 43, 210, 22, 64, 26, 121, 32, 37, 233, 41, 115, 180, 34, 167, 229, 129, 83, 10, 124, 3, 173, 120, 71, 232, 185, 29, 171, 36, 98, 110, 133, 231, 222, 221, 45, 175, 249, 146, 182, 250, 215, 162, 237, 14, 128, 157, 136, 166, 86, 184, 228, 50, 219, 59, 246, 148, 11, 123, 54, 103, 21, 188, 68, 16, 111, 145, 197, 254, 235, 97, 198, 241, 105, 179, 224, 255, 51, 113, 92, 248, 94, 140, 201, 69, 28, 67, 220, 76, 102, 217, 47, 169, 91, 114, 134, 13, 194, 2, 60, 119, 125, 164, 202, 216, 24, 212, 183, 239, 172, 193, 112, 80, 214, 87, 96, 56, 236, 144, 159, 155, 143, 227, 240, 150, 203, 213, 39, 101, 65, 170, 218, 149, 12, 226, 72, 126, 18, 7, 195, 191, 244, 160, 106, 208 };

Word S_f(Word in)
{
	return (Sbox[in >> 8] << 8) | Sbox[in & 0xff];
}



Word P_f(Word in)
{
	int r = 3;
	//std::cout << "in " << in << "\n";
	Word out = 0;
	out |= (in >> 8) & 0xff;
	out |= (in & 0xff) << 8;
	out ^= out >> 8;
	//std::cout << "out " << out << "\n";

	
	Word out2 = 0;
	out2 |= out >> r;
	out2 |= out << (16 - r);
	//std::cout << "out2 " << out2 << "\n";

	return out2;
}

Word r(Word in, RKey kin)
{
	RKey k = kin;
	in ^= (k & 0xffff) ^ ((k >> 16) & 0xffff);
	return P_f(S_f(in));
}

template<Byte which>
RKey getMask(Key k)
{
	RKey w = (k & 0xffffffff) ^ ((k >> 32) & 0xffffffff);
	RKey out = w ^ (S_f((Sbox[which] << 4 ) ^ ((w >> 16) & 0xffff)) ^ (S_f((Sbox[~which] << 4) ^ (w & 0xffff) << 16)));
	return out;
}


RKey ksch(Key k, int i)
{
	// Smash the key based on the round number :D :D
	RKey r;
	
	Key in = k;
	switch (i % 255)
	{

		case 0:
			r = getMask<167>(in);

		case 1:
			r = getMask<97>(in);

		case 2:
			r = getMask<125>(in);

		case 3:
			r = getMask<68>(in);

		case 4:
			r = getMask<20>(in);

		case 5:
			r = getMask<46>(in);

		case 6:
			r = getMask<104>(in);

		case 7:
			r = getMask<242>(in);

		case 8:
			r = getMask<222>(in);

		case 9:
			r = getMask<172>(in);

		case 10:
			r = getMask<203>(in);

		case 11:
			r = getMask<103>(in);

		case 12:
			r = getMask<16>(in);

		case 13:
			r = getMask<22>(in);

		case 14:
			r = getMask<80>(in);

		case 15:
			r = getMask<200>(in);

		case 16:
			r = getMask<60>(in);

		case 17:
			r = getMask<91>(in);

		case 18:
			r = getMask<234>(in);

		case 19:
			r = getMask<141>(in);

		case 20:
			r = getMask<155>(in);

		case 21:
			r = getMask<162>(in);

		case 22:
			r = getMask<72>(in);

		case 23:
			r = getMask<44>(in);

		case 24:
			r = getMask<12>(in);

		case 25:
			r = getMask<95>(in);

		case 26:
			r = getMask<7>(in);

		case 27:
			r = getMask<151>(in);

		case 28:
			r = getMask<197>(in);

		case 29:
			r = getMask<195>(in);

		case 30:
			r = getMask<188>(in);

		case 31:
			r = getMask<61>(in);

		case 32:
			r = getMask<251>(in);

		case 33:
			r = getMask<51>(in);

		case 34:
			r = getMask<179>(in);

		case 35:
			r = getMask<239>(in);

		case 36:
			r = getMask<156>(in);

		case 37:
			r = getMask<10>(in);

		case 38:
			r = getMask<178>(in);

		case 39:
			r = getMask<122>(in);

		case 40:
			r = getMask<193>(in);

		case 41:
			r = getMask<173>(in);

		case 42:
			r = getMask<44>(in);

		case 43:
			r = getMask<216>(in);

		case 44:
			r = getMask<129>(in);

		case 45:
			r = getMask<4>(in);

		case 46:
			r = getMask<207>(in);

		case 47:
			r = getMask<171>(in);

		case 48:
			r = getMask<128>(in);

		case 49:
			r = getMask<44>(in);

		case 50:
			r = getMask<213>(in);

		case 51:
			r = getMask<28>(in);

		case 52:
			r = getMask<21>(in);

		case 53:
			r = getMask<91>(in);

		case 54:
			r = getMask<197>(in);

		case 55:
			r = getMask<171>(in);

		case 56:
			r = getMask<208>(in);

		case 57:
			r = getMask<246>(in);

		case 58:
			r = getMask<10>(in);

		case 59:
			r = getMask<84>(in);

		case 60:
			r = getMask<5>(in);

		case 61:
			r = getMask<153>(in);

		case 62:
			r = getMask<43>(in);

		case 63:
			r = getMask<28>(in);

		case 64:
			r = getMask<44>(in);

		case 65:
			r = getMask<24>(in);

		case 66:
			r = getMask<20>(in);

		case 67:
			r = getMask<136>(in);

		case 68:
			r = getMask<30>(in);

		case 69:
			r = getMask<137>(in);

		case 70:
			r = getMask<141>(in);

		case 71:
			r = getMask<172>(in);

		case 72:
			r = getMask<38>(in);

		case 73:
			r = getMask<8>(in);

		case 74:
			r = getMask<171>(in);

		case 75:
			r = getMask<46>(in);

		case 76:
			r = getMask<113>(in);

		case 77:
			r = getMask<19>(in);

		case 78:
			r = getMask<25>(in);

		case 79:
			r = getMask<248>(in);

		case 80:
			r = getMask<230>(in);

		case 81:
			r = getMask<181>(in);

		case 82:
			r = getMask<223>(in);

		case 83:
			r = getMask<218>(in);

		case 84:
			r = getMask<168>(in);

		case 85:
			r = getMask<30>(in);

		case 86:
			r = getMask<18>(in);

		case 87:
			r = getMask<51>(in);

		case 88:
			r = getMask<149>(in);

		case 89:
			r = getMask<187>(in);

		case 90:
			r = getMask<228>(in);

		case 91:
			r = getMask<101>(in);

		case 92:
			r = getMask<232>(in);

		case 93:
			r = getMask<249>(in);

		case 94:
			r = getMask<38>(in);

		case 95:
			r = getMask<237>(in);

		case 96:
			r = getMask<53>(in);

		case 97:
			r = getMask<52>(in);

		case 98:
			r = getMask<173>(in);

		case 99:
			r = getMask<135>(in);

		case 100:
			r = getMask<240>(in);

		case 101:
			r = getMask<37>(in);

		case 102:
			r = getMask<212>(in);

		case 103:
			r = getMask<12>(in);

		case 104:
			r = getMask<230>(in);

		case 105:
			r = getMask<97>(in);

		case 106:
			r = getMask<22>(in);

		case 107:
			r = getMask<3>(in);

		case 108:
			r = getMask<164>(in);

		case 109:
			r = getMask<181>(in);

		case 110:
			r = getMask<53>(in);

		case 111:
			r = getMask<154>(in);

		case 112:
			r = getMask<118>(in);

		case 113:
			r = getMask<179>(in);

		case 114:
			r = getMask<39>(in);

		case 115:
			r = getMask<104>(in);

		case 116:
			r = getMask<100>(in);

		case 117:
			r = getMask<9>(in);

		case 118:
			r = getMask<72>(in);

		case 119:
			r = getMask<71>(in);

		case 120:
			r = getMask<81>(in);

		case 121:
			r = getMask<22>(in);

		case 122:
			r = getMask<134>(in);

		case 123:
			r = getMask<4>(in);

		case 124:
			r = getMask<87>(in);

		case 125:
			r = getMask<38>(in);

		case 126:
			r = getMask<8>(in);

		case 127:
			r = getMask<129>(in);

		case 128:
			r = getMask<100>(in);

		case 129:
			r = getMask<135>(in);

		case 130:
			r = getMask<225>(in);

		case 131:
			r = getMask<206>(in);

		case 132:
			r = getMask<132>(in);

		case 133:
			r = getMask<194>(in);

		case 134:
			r = getMask<30>(in);

		case 135:
			r = getMask<86>(in);

		case 136:
			r = getMask<167>(in);

		case 137:
			r = getMask<179>(in);

		case 138:
			r = getMask<79>(in);

		case 139:
			r = getMask<224>(in);

		case 140:
			r = getMask<96>(in);

		case 141:
			r = getMask<246>(in);

		case 142:
			r = getMask<64>(in);

		case 143:
			r = getMask<152>(in);

		case 144:
			r = getMask<156>(in);

		case 145:
			r = getMask<56>(in);

		case 146:
			r = getMask<162>(in);

		case 147:
			r = getMask<88>(in);

		case 148:
			r = getMask<94>(in);

		case 149:
			r = getMask<21>(in);

		case 150:
			r = getMask<225>(in);

		case 151:
			r = getMask<60>(in);

		case 152:
			r = getMask<125>(in);

		case 153:
			r = getMask<138>(in);

		case 154:
			r = getMask<74>(in);

		case 155:
			r = getMask<60>(in);

		case 156:
			r = getMask<52>(in);

		case 157:
			r = getMask<168>(in);

		case 158:
			r = getMask<251>(in);

		case 159:
			r = getMask<57>(in);

		case 160:
			r = getMask<160>(in);

		case 161:
			r = getMask<230>(in);

		case 162:
			r = getMask<48>(in);

		case 163:
			r = getMask<157>(in);

		case 164:
			r = getMask<226>(in);

		case 165:
			r = getMask<167>(in);

		case 166:
			r = getMask<11>(in);

		case 167:
			r = getMask<211>(in);

		case 168:
			r = getMask<64>(in);

		case 169:
			r = getMask<50>(in);

		case 170:
			r = getMask<4>(in);

		case 171:
			r = getMask<193>(in);

		case 172:
			r = getMask<231>(in);

		case 173:
			r = getMask<27>(in);

		case 174:
			r = getMask<3>(in);

		case 175:
			r = getMask<208>(in);

		case 176:
			r = getMask<13>(in);

		case 177:
			r = getMask<211>(in);

		case 178:
			r = getMask<51>(in);

		case 179:
			r = getMask<193>(in);

		case 180:
			r = getMask<140>(in);

		case 181:
			r = getMask<94>(in);

		case 182:
			r = getMask<168>(in);

		case 183:
			r = getMask<243>(in);

		case 184:
			r = getMask<84>(in);

		case 185:
			r = getMask<128>(in);

		case 186:
			r = getMask<180>(in);

		case 187:
			r = getMask<32>(in);

		case 188:
			r = getMask<30>(in);

		case 189:
			r = getMask<145>(in);

		case 190:
			r = getMask<173>(in);

		case 191:
			r = getMask<91>(in);

		case 192:
			r = getMask<188>(in);

		case 193:
			r = getMask<243>(in);

		case 194:
			r = getMask<112>(in);

		case 195:
			r = getMask<130>(in);

		case 196:
			r = getMask<47>(in);

		case 197:
			r = getMask<110>(in);

		case 198:
			r = getMask<20>(in);

		case 199:
			r = getMask<227>(in);

		case 200:
			r = getMask<201>(in);

		case 201:
			r = getMask<0>(in);

		case 202:
			r = getMask<117>(in);

		case 203:
			r = getMask<125>(in);

		case 204:
			r = getMask<153>(in);

		case 205:
			r = getMask<30>(in);

		case 206:
			r = getMask<118>(in);

		case 207:
			r = getMask<111>(in);

		case 208:
			r = getMask<69>(in);

		case 209:
			r = getMask<235>(in);

		case 210:
			r = getMask<107>(in);

		case 211:
			r = getMask<187>(in);

		case 212:
			r = getMask<206>(in);

		case 213:
			r = getMask<240>(in);

		case 214:
			r = getMask<54>(in);

		case 215:
			r = getMask<147>(in);

		case 216:
			r = getMask<108>(in);

		case 217:
			r = getMask<122>(in);

		case 218:
			r = getMask<32>(in);

		case 219:
			r = getMask<101>(in);

		case 220:
			r = getMask<39>(in);

		case 221:
			r = getMask<186>(in);

		case 222:
			r = getMask<139>(in);

		case 223:
			r = getMask<29>(in);

		case 224:
			r = getMask<43>(in);

		case 225:
			r = getMask<227>(in);

		case 226:
			r = getMask<40>(in);

		case 227:
			r = getMask<187>(in);

		case 228:
			r = getMask<86>(in);

		case 229:
			r = getMask<167>(in);

		case 230:
			r = getMask<220>(in);

		case 231:
			r = getMask<27>(in);

		case 232:
			r = getMask<199>(in);

		case 233:
			r = getMask<0>(in);

		case 234:
			r = getMask<108>(in);

		case 235:
			r = getMask<196>(in);

		case 236:
			r = getMask<58>(in);

		case 237:
			r = getMask<193>(in);

		case 238:
			r = getMask<17>(in);

		case 239:
			r = getMask<154>(in);

		case 240:
			r = getMask<237>(in);

		case 241:
			r = getMask<33>(in);

		case 242:
			r = getMask<126>(in);

		case 243:
			r = getMask<193>(in);

		case 244:
			r = getMask<246>(in);

		case 245:
			r = getMask<132>(in);

		case 246:
			r = getMask<96>(in);

		case 247:
			r = getMask<138>(in);

		case 248:
			r = getMask<73>(in);

		case 249:
			r = getMask<44>(in);

		case 250:
			r = getMask<88>(in);

		case 251:
			r = getMask<8>(in);

		case 252:
			r = getMask<58>(in);

		case 253:
			r = getMask<226>(in);

		case 254:
			r = getMask<149>(in);

		case 255:
			r = getMask<143>(in);
	}

	i %= 4;

	// 255 isn't divisible by 4 so theoretically since 255 * 4 = 1020
	// key repeats after 1020 rounds

	k ^= r;
	k ^= ((Key)r) << 32;

	k |= 0xff << 24;
	k |= 0xffULL << (24 + 32);

	if (i == 0)
	{
		r = k & 0xffffffff;
		r ^= 1162466901;
		r ^= r >> 16;
		r *= 3726821653;
	}
	if (i == 1)
	{
		r = ((k >> 32) & 0xffffffff) ^ (k & 0xffffffff);
		r ^= 3811777446;
		r = (r * 1240568533);
	}
	if (i == 2)
	{
		r = ((k >> 32) & 0xffffffff) ^ (k & 0xffffffff);
		r ^= 3915669785;
		r = (r * 1247778533);
	}
	if (i == 3)
	{
		r = ((k >> 32) & 0xffffffff) ^ (k & 0xffffffff);
		r ^= 3140176925;
		r = (r * 1934965865);
	}


	return r;
}

Word encrypt(Word in, Key k)
{
	Word out = in;
	for (int i = 0; i < rounds; i++)
	{
		out = r(out, ksch(k, i));
	}
	return out;
}



Word oracle(Word in)
{
	return encrypt(in, key);
}

Word flag[21];

void readflag()
{
	flag[21] = 0;
	std::ifstream myfile("flag.txt");
	if (myfile.is_open())
	{
		std::string line;
		while (std::getline(myfile, line))
		{
			std::cout << line << '\n' << line.size() << "\n";
			for (int i = 0; i < line.size(); i += 2)
			{
				flag[i / 2] = oracle(*(Word*)&line[i]);
			}

		}
		myfile.close();
	}
}

Word getRand()
{
	Word w;
	static std::random_device rd;
	return rd();
}