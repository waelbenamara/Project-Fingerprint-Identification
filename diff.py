from Fingerprint import FingerPrint
import pickle
fp=FingerPrint("./Fingerprints/test/")
#fp.run()
fp.dataload()
#x=fp.get_arr()
fp.data_comp()
fp.train_comparaison()
#fp.hash()
#fp.combine()
#p.train_detection()
#fp.train_comparaison()
