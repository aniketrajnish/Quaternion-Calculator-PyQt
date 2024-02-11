from quaternion import Quaternion

def main():
    '''
    Main function to demonstrate the use of the Quaternion class.
    '''
    q1 = Quaternion(1, (2, 3, 4))
    print("q1 = ", q1) 
    q2 = Quaternion(angle=60, axis=(1, 2, 4))
    print("q2 = ", q2)
    
    q3 = q1 + q2
    print("q1 + q2 = ", q3)
    
    q4 = q1 - q2
    print("q1 - q2 = ", q4)
    
    q5 = q1 * 3
    print("q1 * 3 = ", q5)
    
    q15 = 3 * q1
    print("3 * q1 = ", q15)
    
    q6 = q1 * q2
    print("q1 * q2 = ", q6)
    
    s1 = q1.magnitude()
    print("Magnitude of q1 = ", s1)
    s2 = q2.magnitude()
    print("Magnitude of q2 = ", s2)
    
    n1 = q1.normalize()
    print("q1 normalized = ", n1)
    n2 = q2.normalize()
    print("q2 normalized = ", n2)
    
    q14 = q1.difference(q2)
    print("Difference of q1 and q2 = ", q14)
    
    q7 = q1.dot(q2)
    print("q1 dot q2 = ", q7)
    q8 = q2.dot(q1)
    print("q2 dot q1 = ", q8)
    
    q9 = -q1
    print("Conjugate of q1 = ", q9)
    q10 = -q2
    print("Conjugate of q2 = ", q10)
    
    q11 = ~q1
    print("Inverse of q1 = ", q11)
    q12 = ~q2
    print("Inverse of q2 = ", q12)
    
    pt = (1, 2, 3)
    pt2 = q1.transform(pt)
    print("Transformed pt = ", pt2)
    
    q13 = q1.slerp(q2, 0.5)
    print("Slerp of q1 and q2 at t = 0.5 = ", q13)   
    
    q15 = q2.toAngleAxis()
    print("q2 as angle-axis = ", q15)
    
main()