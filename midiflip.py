#Ret Samys, creator of this program, can be found at RetSamys.deviantArt.com
#Please feel free to change anything or to correct me or to make requests... I'm a really bad coder. =)
#Watch Andrew Huang's video here: https://www.youtube.com/watch?v=4IAZY7JdSHU

changecounter=0
path="for_elise_by_beethoven.mid"
print """Welcome to my horribly inefficient program to tonal invert MIDI files according to Andrew Huang's #MIDIFLIP challenge as seen on https://www.youtube.com/watch?v=4IAZY7JdSHU
"""
pth=raw_input("Please enter your MIDI file's path here (save the file in the same directory as this program if you want to avoid typing the entire path): ")
if pth!="":path=pth
print "Program running"
print "You may abort any time by hitting CTRL+C"
try:
    f=open(path,"rb")
except:
    try:
        f=open(path+".mid","rb")
    except:
        print "Sorry, but are you sure this is where the file is?"
midi=f.read()
writeme="".join(midi.split("MTrk")[0]) #final string to be written into new file
for i in midi.split("MTrk")[1:]: #skip header chunk and jump directly into track chunk
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
            if ord(i[4:][byte])>=144 and ord(i[4:][byte])<=159: #check for note on event
                byte+=1 #go to note byte
                try: #skipped if lastnote is not defined
                    offset+=(ord(lastnote)-ord(i[4:][byte]))*2 #calculate offset
                except NameError:
                    pass
                lastnote=i[4:][byte] #set current note to compare to next note before it's changed!
                i[byte+4]=chr(ord(i[4:][byte])+offset) #change note
                #journey to note off starts here
                for offbyte in range(len(i[byte+4:])):
                    #if i[byte+4:][offbyte]==i[4:][byte-1] and i[byte+4:][offbyte+1]==lastnote: #check the same channel if the same note is off
                    if ord(i[byte+4:][offbyte])>=128 and ord(i[byte+4:][offbyte])<=137 and i[byte+4:][offbyte+1]==lastnote: #check if the same note is off
                        i[byte+4+offbyte+1]=chr(ord(i[byte+4:][offbyte+1])+offset) #change note
                        changecounter+=1
                        break
                    elif ord(i[byte+4:][offbyte])==123: #all notes off
                        changecounter+=1
                        break
                    elif ord(i[byte+4:][offbyte])>=160 and ord(i[byte+4:][offbyte])<=175 and i[byte+4:][offbyte+1]==lastnote: #polyphonic aftertouch - just in case? Urgh, I don't actually understand this enough, when is this activated and is there a way to deactivate!?!?
                        i[offbyte+5]=chr(ord(i[byte+4:][offbyte+1])+offset) #change note
                    else:
                        pass
                byte+=1 #skip velocity byte
            else:
                pass
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
