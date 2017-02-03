#Ret Samys, creator of this program, can be found at RetSamys.deviantArt.com
#Please feel free to change anything or to correct me or to make requests... I'm a really bad coder. =)
#Watch Andrew Huang's video here: https://www.youtube.com/watch?v=4IAZY7JdSHU

changecounter=0
path="for_elise_by_beethoven.mid"
print """Welcome to my horribly inefficient program to tonal invert MIDI files according to Andrew Huang's #MIDIFLIP challenge as seen on https://www.youtube.com/watch?v=4IAZY7JdSHU
"""
pth=raw_input("Please enter your MIDI file's path here (save the file in the same directory as this program if you want to avoid typing the entire path): ")
if pth!="":path=pth
try:
    f=open(path,"rb")
except:
    try:
        f=open(path+".mid","rb")
    except:
        print "Sorry, but are you sure this is where the file is?"
cset=raw_input("As a standard setting, this program will flip all notes around C', which will flip the 'hands'. To use this mode press enter. You can use the old mode, which keeps the 'hands' where they are, but also creates a whole bunch of errors, by entering anything at all: ")
print "Program running"
print "You may abort any time by hitting CTRL+C"

midi=f.read()
writeme="".join(midi.split("MTrk")[0]) #final string to be written into new file
for i in midi.split("MTrk")[1:]: #skip header chunk and jump directly into track chunk
    print "Editing Track "+str(midi.split("MTrk").index(i))+" of "+str(len(midi.split("MTrk"))-1)
    lowcount=0
    highcount=0
    i=list(i) #split string into list of characters
    delta=True #default value for checking delta_time
    offset=0 #default value for flipping pitch according to last event - since there is no such event at the beginning of a track
    for byte in range(len(i[4:])): #skip length bytes
        if delta: #delta_time checking mode
            if ord(i[4:][byte])>127: #determine if this is the last byte of the variable-length quantity for delta_time
                delta=False #found last byte! next byte should be event
            else:
                pass
        else: #event checking mode
            if ord(i[4:][byte])==255 and ord(i[4:][byte+1])==81 and ord(i[4:][byte+2])==3: #check for set tempo meta-event
                byte+=5 #skip set tempo meta-event
            elif ord(i[4:][byte])>=144 and ord(i[4:][byte])<=159: #check for note on event
                byte+=1 #go to note byte
                if cset=="":
                    offset=(60-ord(i[4:][byte]))*2 #calculate offset to c'
                else:
                    try: #skipped if lastnote is not defined
                         offset+=(ord(lastnote)-ord(i[4:][byte]))*2 #calculate offset
                    except NameError:
                        pass

                lastnote=i[4:][byte] #set current note to compare to next note before it's changed!
                try:i[byte+4]=chr(ord(i[4:][byte])+offset) #change note
                except:
                    if ord(i[4:][byte])+offset>127:
                        i[byte+4]=chr(127)
                        highcount+=1
                    else:
                        i[byte+4]=chr(0)
                        lowcount+=1
                #journey to note off starts here
                for offbyte in range(len(i[byte+4:])):
                    if ord(i[byte+4:][offbyte])==255 and ord(i[byte+4:][offbyte+1])==81 and ord(i[byte+4:][offbyte+1])==3: #check for set tempo meta-event
                        offbyte+=5 #skip set tempo meta-event
                    elif ord(i[byte+4:][offbyte])>=128 and ord(i[byte+4:][offbyte])<=137 and i[byte+4:][offbyte+1]==lastnote: #check if the same note is off
                        try:i[byte+4+offbyte+1]=chr(ord(i[byte+4:][offbyte+1])+offset) #change note
                        except:
                            if ord(i[4:][byte])+offset>127:
                                i[byte+4]=chr(127)
                            else:
                                i[byte+4]=chr(0)
                        changecounter+=1
                        break
                    elif ord(i[byte+4:][offbyte])==123: #all notes off
                        changecounter+=1
                        break
                    elif ord(i[byte+4:][offbyte])>=160 and ord(i[byte+4:][offbyte])<=175 and i[byte+4:][offbyte+1]==lastnote: #polyphonic aftertouch - just in case? Urgh, I don't actually understand this enough, when is this activated and is there a way to deactivate!?!?
                        try:i[offbyte+1+byte+4]=chr(ord(i[byte+4:][offbyte+1])+offset) #change note
                        except:
                            i[offbyte+1+byte+4]=chr(127)
                    else:
                        pass
                byte+=1 #skip velocity byte
            else:
                pass
    if lowcount or highcount:print "WARNING: There were notes out of range: "+str(lowcount)+" too low and "+str(highcount)+" too high."
    writeme=writeme+"MTrk"+"".join(i) #join list of characters to final string
counter=1
path=path.replace(".mid","")
while True:
    try:
        newfile = open(path+"_midiflip_"+str(counter)+".mid")
        newfile.close()
        counter+=1
    except IOError as e:
        newfile = open(path+"_midiflip_"+str(counter)+".mid","wb")
        newfile.write(writeme)
        newfile.close()
        break

print "End of the line..."
print str(changecounter)+" notes changed"
