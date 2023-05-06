from cryptography.fernet import Fernet
import base64

alphabet = '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
payload = b'gAAAAABizN9NSQE_3kGjoID2dD8MLyVf8E3s-K3IeCjacVrkEUFqgqXQWczlQ0LEcPFerBS1A0UN29oUpkHAAufRt4Sp9f7ELyJ_JSFKgfaiHDwpXpHP4ZgTZoNq8PoA5wvygJZbkVuy_qymiT_MW-9LSy9HLQBiQQoG0IbJm_VuxA1xAxtKRXtIsNgryAICMkM6mLHrAKQwRUtAQLAbxNpAelwBRYWbX3pvjYB0s0pjxxdvpyVxNiJcjVDTh6YaLTCgZMW-IpATAoLEtJe-VnxBPIGQp1sDob-TdRLV8r1BHDEuIGOHAuVbwLjkF2EuhfXxXy4PV5SZtRNzAijJTvwLSlulxyG_TsiRI58Z58rBzNFtU6HMj5D_42kk6nxILdhvsP6gs25pRg6GojHultDRqZ-o4gOiDMtHyqihnhIaERAaf05dn8-K32xF1SAnm4l_hJcssgJX5BZZJKv13B4gIhJ9c4KXiwSddPjwxoXokmkfSUUEdLgdAP6gE5hbV29pOgSXC0g0QrNfMQ0GFLW56TB-n1D5-bCP6RFX8XHo77CUe7XoUKMHEEutTbwhStKhoebi6bhb7rD0XVJSll7q10fFq4jwSiiNhDQ5fi69uIXNsorwC3ryriaqueC3mDxPuDNZ5r24p98rqajM-WOrOw88gf47mvcwTBPUaTkROmWRh9pVaJVXKV-r4Jj49D54aEk9tmWSSowkj0m9krIa3v2jGWCBSWalYa68qj-Bf8SEtMR-xWbjxL2C-oHaxPdi2AkTOcfGVutapi9wpio0eyjX0dabqVXehs4yGPoA1lrNs23En8mBS9MlFc0cmO8DQwtPcco_efkdKau2krhkxISFTN4rpJc5vHZg6x92d5Uct23dJSC364F-g6mLBxliKd2tiCxTZHuFZFt7_BgNK7I1egWzkqzUcdD-PQaRUxTjw06gFjaH2Dw3ppoWaV3d5XLcn91BAcW4JUBWLLy8BCCdvlm9QGQbzqDRAFWJpQfrqAzhg3nwnFghZ7inS4yy171AHm7-RFgNXyb4gbTzDmEpZdjMYGXIB_GOFMONsVCAvNmlxpEaggSQ6mxEkrzCTPQh6tJBwRnRarUfHIXuFksQXaft58jqhJhrvymlSBwLwc4_eXPb5VqtnCPCmbA23KB51OG5QPii-OeIWqNq-IU1vJWoZoriqkOZDMTi7ejRM8G26jnsWbcpaAxS92ESv86mxiB3qKAv1PKC_IG4_NuUYzpslJpkbaO4uEzJP5WiDwDG3lu_59-NX0EWoTl5_Hcw0gTThQp8zQKoPgtxY-ZvCNE5pjQ1vkIZAkIGcO_nhyt2xJOUr56zmavbfULx9ozmdXDUdGm5AKf9EVUuyellFhP4GQD3RS0l8Fj4qG7zSKIthlGgS7_qjkEEXr8d-lIEqdJOWNT5hWbog2330n1TGDORd3H2q6KvRnv4lbw3ckbJeYPp0supGk21-wwJEfr1ImWMfwSlG5np4vtxPLjzWXHY0dM9yfKkSriq_c6PKQVG5VChfHcJ3mMOLrjoxHDb8FJktY3SVW0-O1rrLnROiJs2qwIbu4trQnLRuoPKEMHE7ZOiFAt-9xgN4mxWjAss_ipzcplLgocobzSg6cKhhIl5Wuxa7ZMzVGdwRsdEHPrDmMXbI26_TcFKQLz-5wSk6N-TnEg5Sdn64FzoaDKX-ZtX3MbTOoQyczGV9upKZkxTIc4FWbyWqkJs0GySOC3SGiAXORzhEvA1q1Cp3wICU-jjww_szv75HWT2zLxyWldvrAT_rC4SgyqCjnL1Ig-yUQZiLDiGEGARBG1XTAylrE3vHRBRH2eavYomnIKwAU_WjDbgUaw3mxDqULQWiMt7AeB99MjDw1QDxZappYtYZmFDyz0NPSwGNHqb05HivG56rMDAyiX8gKbgWcR5bu6i7nL6WppXGMUb3gP-aD2REfm30HHIjJVY0HX5dCI7Ol2qyZK7eUSiiMS0Qnjo1x-J6Ks8qNI2NbFmTF0TnJOaVS71KjKLGgTH4XeCXnAtx-eoHC6ImPVAXZiaU_OZdglhPIcjAeOjdd5Tjj8ipKakRfYPAgnYb7dThWMOInF6_-pS1F_ygWu2yHnVTj4mUPdBgGeO_m9OvDdHbyiz0vTlQ_g-kPuISaZLryWKXVx8eDXCprRCniof1vnopCt_DTeKZONrTFjq7hvl9fLVksLAHJJ-e2pGLQnOcgue4NGfnUfGI9eUNLyeG9jahx-ydtSIsV7cc-EQdDjJF6P20kY_vO-Qx8ZjhvFuNhWh3NQyVE282GGL1QBI0jknQ-uuMDC1YFDzuxLE9kwycs_FoL8T7jzzRgVgOYcnFIT4hU2A5lDtHmlqsKFNUGzPPEm-Oa3d5WISADqK08u_78oQnArr2nBFdXj2JodPDDLQdj3kclq9mQzz_goDeb6aq7rBsTUzRzP_1Jsrv1jqOqGtWXbJQWcgd8vANds79bh8nEgTA5Gdq69TsJo9PjXvdwkQgLVAnkSBoNoOF7h1_ph0vQGadv3d3RkqW-02V_mFuMFIC-pyg2QnHcAtkON45AejgsS92nAso7Mf-xXJFkrnPItuun2MYXvqf2-86BBsiF_3TNCIi2wLY3dmiAj2Bzw9FQ-3k1Nv_FXTNjEUqCaUGfsMO0lfSQcigr2169PZyc7ck_gHF8y-oXjWRcywXzLEEEs5yscjEycedfur1FK-cYvUsIghht1yJhQRWGDrhvP5PzvSkJeCgXWt1gxoEF7uvMqDSUd1jUoFW7te_e_u68uXeGZTooAsGxSo11c3AS-QjyEiNbw='


def derivePassword():
    kw = ['~#+', 'v~s', 'r~st', '%xvt#', 'st%tr%x\'t']
    userKeyInput = input('Enter the key: ')  # 7-digit integer

    try:
        retrievePasswordKey = list(map(int, list(userKeyInput)))
        # retrievePasswordKey = list(str(10*0) + len(kw[2]) + str(2**0) + len(kw[0]) + '2' + len("orz) + '0')

        ct = kw[retrievePasswordKey[0]] + kw[retrievePasswordKey[1]] + kw[retrievePasswordKey[2]] + \
            kw[retrievePasswordKey[3]] + kw[retrievePasswordKey[4]] + \
            kw[retrievePasswordKey[5]] + kw[retrievePasswordKey[6]]
        # return ROT(ct, s)
        return 'defaultplaceholderkeystringabcde'
    except:
        if max(list(map(int, list(userKeyInput)))) >= len(kw):
            print('Key digits out of range!')
        else:
            print('Invalid key format!')
        exit()


key_str = derivePassword()
key_base64 = base64.b64encode(key_str.encode())
f = Fernet(key_base64)

try:
    d = f.decrypt(payload)
except:
    print('The provided key was not correct!\nDECRYPTION FAILED.')
    exit()

solution = d.decode()  # decrypted solution
print(solution)


def ROT(ct, s):
    pt = ''
    for c in ct:
        index = alphabet.find(c)
        original_index = (index + s) % len(alphabet)
        pt = pt + alphabet[original_index]
    return pt
# s = 1 (mod 2), s = 7 (mod 11), 7 < |s| < 29
# ROT|s| used to create password ciphertext


def solutionDecrypt(cipher):
    cipher = cipher.split('\n')

    def c(l):
        b = ''
        l = l.split()
        if len(l) > 0:
            for t in l:
                if t == 'codetiger':
                    b += '1'
                elif t == 'orz':
                    b += '0'
            return chr(int(b, 2))
        else:
            return ''

    s = ''
    for l in cipher:
        s += c(l)
    return s
