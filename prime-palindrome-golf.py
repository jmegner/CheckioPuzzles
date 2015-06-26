def golf(n):    
    for i in range(n + 1, 99999):
        if isPalindrome(i) and isPrime(i):
            return i
            
            
def isPrime(n):
    if n < 2:
        return False
    for i in range(2, n // 2):        
        if n % i == 0:
            return False
    return True
    
    
def isPalindrome(num):
    numStr = str(num)
    return numStr == numStr[::-1]