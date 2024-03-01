#this function check palindrome string
num =122
temp =num
newnum=0
while(num>0):
    digit = num%10
    newnum = (newnum*10) + digit
    num = num//10
    
if(temp==newnum):
    print("palindrome")
else:
    print("not palindrome")





