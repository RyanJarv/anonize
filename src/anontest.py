from ctypes import *
import time

def pretty(s, title):
    print("{}:\n".format(title))
    for line in s.decode().split('\n'):
        print("         {}".format(line))

cdll.LoadLibrary('./anonize2/libanon.so')
cdll.LoadLibrary('libc.so.6')

libanon = CDLL('libanon.so')
libc = CDLL('libc.so.6')

libanon.initAnonize()
RAVK = create_string_buffer(2048)
RASK = create_string_buffer(2048)
libanon.makeKey.argtypes = [c_char_p, c_char_p]
libanon.makeKey(RAVK, RASK)
print("{}\n\n".format(RAVK.value.decode()));
print("{}\n\n".format(RASK.value.decode()));

libanon.makeCred.restype = c_char_p
libanon.makeCred.argtypes = [c_char_p]
uid = "abhi@virginia.edu".encode()
precred = libanon.makeCred(uid)

libanon.registerUserMessage.restype = c_char_p
libanon.registerUserMessage.argtypes = [c_char_p, c_char_p]
reg1 = libanon.registerUserMessage(precred, RAVK.value)

libanon.registerServerResponse.restype = c_char_p
libanon.registerServerResponse.argtypes = [c_char_p, c_char_p, c_char_p]
reg2 = libanon.registerServerResponse(uid, reg1, RASK.value)

libanon.registerUserFinal.restype = c_char_p
libanon.registerUserFinal.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p]
cred = libanon.registerUserFinal(uid, reg2, precred, RAVK.value)
pretty(cred, "cred")

emails = b"abhi@virginia.edu\nbob\nalice\nAnita\n87f98s8d97\nTasiuhfdiuashdf\neiufwueh";
emails2 = b"efwefwe\nbdfsdfwew\nalfwew2ice\nAn2ita\nsdfsDfsdf\nedfsdfwewwueh";

class survey(Structure):
     _fields_ = [("vid", c_char_p),
                 ("vavk", c_char_p),
                 ("sigs", c_char_p),
                 ("cnt", c_int),
                 ("vask", c_char_p)]

class survey_response(Structure):
    _fields_ = [("msg", c_char_p),
                ("token", c_char_p)]

s = survey()

print(" ********************************************")

uidsig = c_char_p()

libanon.createSurvey.restype = c_int
libanon.createSurvey.argtypes = [POINTER(survey)]
if libanon.createSurvey(s) != 1:
    print("!!!! ERROR CREATING Survey!")
    exit(1)

libanon.extendSurvey.restype = c_int
libanon.extendSurvey.argtypes = [c_char_p, POINTER(survey)]
r = libanon.extendSurvey(emails, s);
if  r != 7:
    print(r)
    print("!!!! ERROR CREATING Survey!")
    exit(1)

if libanon.extendSurvey(emails2, s) != 6:
    print("!!!! ERROR CREATING Survey!")
    exit(1)

pretty(s.vid,"vid");
pretty(s.vavk,"vavk");
pretty(s.sigs,"sigs");


if uid not in s.sigs:
    print("!!! Error making survey!")
    exit(1)
else:
    uidsig = s.sigs.lstrip(uid + b',')
    pretty(uidsig, 'uidsig')
    print(len(uidsig))

    start = time.time()
    libanon.submitMessage.restype = c_char_p
    libanon.submitMessage.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p]
    msg = libanon.submitMessage(b"[\"hello test\"]", cred, RAVK.value, uidsig, s.vid, s.vavk);
    end = time.time()
    taken = start - end
    print("   elapsed: {}".format(taken))

    pretty(msg,"msg");
    pretty(RAVK.value,"ravk");
    pretty(s.vid,"s.vid");
    pretty(s.vavk,"s.vavk");

    sr = survey_response()

    libanon.verifyMessage.restype = c_int
    libanon.verifyMessage.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, POINTER(survey_response)]
    r = libanon.verifyMessage(msg, RAVK.value, s.vid, s.vavk, sr)
    if not r:
        print(" === fail ===")
        exit(1)
    else:
        print(" === SUCCEED ===")

    libanon.freeSurvey.argtypes = [POINTER(survey)]
    libanon.freeSurvey(s)

    libanon.freeSurveyResponse.argtypes = [POINTER(survey_response)]
    libanon.freeSurveyResponse(sr)

    del msg
