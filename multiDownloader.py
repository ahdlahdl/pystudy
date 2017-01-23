import urllib.request, urllib.parse, urllib.error
import _thread
import time
import sys, traceback

progressCnt = 0
completeCnt = 0
failCnt = 0

TARGET_URLS = [
	"http://docs.spring.io/spring-boot/docs/current/reference/pdf/spring-boot-reference.pdf",
	"http://pdf.th7.cn/down/files/1603/Spring%20Boot%20in%20Action.pdf",
	"https://qconsf.com/sf2012/dl/qcon-sanfran-2012/slides/KevinBourrillion_AnOverviewOfGuavaGoogleCoreLibrariesForJava.pdf"
	]

def downloadUrl(threadName, targetUrl, fileNamePrefix):
	global completeCnt, failCnt, progressCnt
	progressCnt += 1
	try:
		print ("%s: %s, start download... %s" % ( threadName, time.ctime(time.time()), targetUrl ))
		urllib.request.urlretrieve(targetUrl, fileNamePrefix + targetUrl.split("/")[-1])
		print ("%s: %s, download completed... %s" % ( threadName, time.ctime(time.time()), targetUrl ))
		completeCnt += 1
	except:
		print ("%s: %s, download failed... %s" % ( threadName, time.ctime(time.time()), targetUrl ))
		failCnt += 1
	progressCnt -= 1

def monitor(threadName):
	global completeCnt, failCnt, progressCnt
	print("start monitor thread")
	while 1:
		time.sleep(1)
		print("progress:%s, complete:%s, fail:%s" % (progressCnt, completeCnt, failCnt))
	
# Create two threads as follows
try:
	_thread.start_new_thread( monitor, ("Thread-monitor", ) )
	delay = 1
	i = 0
	while i < len(TARGET_URLS):
		targetUrl = TARGET_URLS[i]
		_thread.start_new_thread( downloadUrl, ("Thread-" + str(i), targetUrl, "") )
		if i % 5 == 0:
			time.sleep(delay)
		i += 1

except:
	print("Unexpected error:", sys.exc_info()[0])
	traceback.print_exc(file=sys.stdout)

while 1:
	time.sleep(2)
	if completeCnt + failCnt >= len(TARGET_URLS):
		break

print("end")
