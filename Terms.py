#this file represents the back end of the project that contains all of the 
#objects that compute equation values and diferentiate equations, etc...

from abc import ABCMeta, abstractmethod
import math
import decimal
import copy

from tkinter import *
#from numpy import*
#from Utility import *
import multiprocessing as mp

#add, sub, mult methods?
#from Utility import * - is there na importing error???

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))
    
    
def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)


class Term(object):    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def generatePoint(self, x):
        pass
        
    def generatePoints(self, start, stop, step):
        try :
            l = []
            i = start
            while i <= stop:
                l.append(self.generatePoint(i))
                i += step
            return l
        except:
            return None
        
    @abstractmethod
    def deriv(self):
        pass
      
    
class Sin(Term):
    
    def generatePoint(self,x):
        return (x, math.sin(x))
        
    def deriv(self):
        return Cos()
        
    def __repr__(self):
        return "sin(x)"
        
        
        
class Cos(Term):
    
    def generatePoint(self,x):
        return (x, math.cos(x))
    
    def deriv(self):
        return Product(Decimal(-1),Sin())
        
    def __repr__(self):
        return "cos(x)"
        
class Tan(Term):
    
    def generatePoint(self,x):
        try:
            return (x, math.tan(x))
        except:
            return None
        
    def deriv(self):
        return Composition(Sec(), Power(2))
        
    def __repr__(self):
        return "tan(x)"
        
class Sec(Term):
    
    def generatePoint(self,x):
        try:
            return (x, 1/math.cos(x))
        except:
            return None
        
    def deriv(self):
        return Product(Sec(), Tan())
        
    def __repr__(self):
        return "sec(x)"
        
class Csc(Term):
    
    def generatePoint(self,x):
        try:
            return (x, 1/math.sin(x))
        except:
            return None
        
    def deriv(self):
        return Product(Decimal(-1),Csc(), Cot())
        
    def __repr__(self):
        return "csc(x)"
        
    
        
class Cot(Term):
    
    def generatePoint(self,x):
        try:
            return (x, 1/math.tan(x))
        except:
            return None
        
    def deriv(self):
        return Product(Decimal(-1), Composition(Csc(), Power(2)) )
        
    def __repr__(self):
        return "cot(x)"
         
class ArcSin(Term):
    
    def generatePoint(self,x):
        try:
            return (x, math.asin(x))
        except:
            return None
        
    def deriv(self):
        return Composition(Sum(Decimal(1), \
        Product(Decimal(-1),Power(2))), Power(-1/2))
        
    def __repr__(self):
        return "arcsin(x)"
        
class ArcCos(Term):
    
    def generatePoint(self,x):
        try:
            return (x, math.acos(x))
        except:
            return None
        
    def deriv(self):
        Product(Decimal(-1), ArcSin().deriv())
        
    def __repr__(self):
        return "arccos(x)"
        
class ArcTan(Term):
    
    def generatePoint(self,x):
        return (x, math.atan(x))
        
    def deriv(self):
        return Composition(Sum(Decimal(1), Power(2)), Power(-1))
        
    def __repr__(self):
        return "arctan(x)"
        
class ArcCsc(Term):
    
    def generatePoint(self,x):
        try:
            return (x, math.asin(1/x))
        except:
            return None
        
    def deriv(self):
        return Product(Decimal(-1), ArcSec().deriv())
    
    def __repr__(self):
        return "arccsc(x)"
        
class ArcSec(Term):
    
    def generatePoint(self,x):
        try:
            return (x, math.acos(1/x))
        except:
            return None
        
    def deriv(self):
        return Composition(Product(Abs(), Composition(Sum(Power(2), \
        Decimal(-1)), Power(1/2))), Power(-1))
        
    def __repr__(self):
        return "arcsec(x)"
    
        
class ArcCot(Term):
    
    def generatePoint(self,x):
        try:
            if x < 0:
                return (x, math.atan(1/x) + math.pi)
            return (x, math.atan(1/x))
        except:
            return None
        
    def deriv(self):
        return Product(Decimal(-1), ArcTan().deriv())
        
    def __repr__(self):
        return "arccot(x)"

class Abs(Term):
    
    def generatePoint(self,x):
        return (x,abs(x))
        
    def deriv(self):
        return Fraction(Abs(), Power(1))
        
    def __repr__(self):
        return "|x|"
        
class Power (Term):
    
    def __init__(self, power = 0):
        
        if almostEqual(power%1, 0):
            power = roundHalfUp(power)
            
        self.power = power 
        
    def generatePoint(self,x):
        y = x**self.power
        if type(y) != complex:
            return (x, y)
        
    def deriv(self):
        
        if almostEqual(self.power,1):
            return Decimal(1)
        return Product(Decimal(self.power), Power(self.power-1))

    def __repr__(self):
        
        if almostEqual(self.power, 1):
            return "x"
        elif almostEqual(self.power, 0):
            return "1"
        elif almostEqual(self.power%1, 0):
            if self.power < 0:
                return "x^(%d)" % roundHalfUp(self.power)
            return "x^%d" % roundHalfUp(self.power)
        else:
            if self.power < 0:
                return "x^(%0.2f)" % self.power
            return "x^%0.2f" % self.power
            
        return "x^%d" % self.power
        
        

    
class Decimal(Term):
    
    def __init__(self, value = 0):
        
        if almostEqual(value%1, 0):
            value = roundHalfUp(value)
            
        self.value = value 
        
    def generatePoint(self,x):
        return (x,self.value)
        
    def deriv(self):
        return Decimal(0)
        
    def __repr__(self):
        
        if almostEqual(self.value%1, 0):
            return "%d" % int(self.value)
        elif almostEqual(self.value, math.e):
            return "e"
        elif almostEqual(self.value, math.pi):
            return u"\u03C0"
        else: 
            return "%0.3f" % self.value
        
        
    def __eq__(self, other):
        if not isinstance(other, Decimal):
            return False
        return other.value == self.value 
    
class Exponent(Term):
    
    def __init__(self, base):
        
        if almostEqual(base%1, 0):
            base = roundHalfUp(base)

        self.base = base 
        
    def generatePoint(self,x):
        return (x,self.base**x)
        
    def deriv(self):
        return Product(Exponent(self.base), Decimal(math.log(self.base)))
        
    def __repr__(self):
        
        if almostEqual(self.base, math.e):
            return "e^x"
        elif almostEqual(self.base%1, 0):
            if self.base < 0:
                return "(%d)^x" % roundHalfUp(self.base)
            return "%d^x" % roundHalfUp(self.base)
        else: 
            if self.base < 0:
                return "(%0.3f)^x" % self.base
            return "%0.3f^x"
            
        
        
        
class NaturalExpo(Exponent):
    
    def __init__(self):
        super().__init__(math.e)
        
    def deriv(self):
        return NaturalExpo()
        
    def __repr__(self):
        return "e^x"
        
class Floor(Term):
    
    def generatePoint(self,x):
        return (x,math.floor(x))
        
    def deriv(self):
        return Decimal(0)
        
    def __repr__(self):
        return "[x]"
        

        
class Log(Term):
    
    def generatePoint(self,x):
        if x > 0:
            return (x,math.log10(x))
        return None
        
    def deriv(self):
        return Fraction(Decimal(1), Product(Decimal(math.log(10)), Id()))
        
    def __repr__(self):
        return "log(x)"


class NaturalLog(Term):
    
    def generatePoint(self,x):
        if x > 0:
            return (x,math.log(x))
        return None
        
    def deriv(self):
        return Fraction (Decimal(1), Id())
        
    def __repr__(self):
        return "ln(x)"
        
class SinH(Term):
    
    def generatePoint(self,x):
        return (x, math.sinh(x))
            
    def deriv(self):
        return CosH()
        
    def  __repr__(self):
        return "sinh(x)"
        
        
class CosH(Term):
    
    def generatePoint(self,x):
        return (x, math.cosh(x))
            
    def deriv(self):
        return SinH()
        
    def  __repr__(self):
        return "cosh(x)"
        
        
class TanH(Term):
    
    def generatePoint(self,x):
        return (x, math.tanh(x))
            
    def deriv(self):
        return Sum (Decimal(1), Product(Decimal(-1), \
        Composition(TanH(), Power(2))))
        
    def  __repr__(self):
        return "tanh(x)"
        
class SecH(Term):
    
    def generatePoint(self,x):
        return (x, 1/math.cosh(x))
            
    def deriv(self):
        return Product(Decimal(-1), TanH(), SecH())
        
    def  __repr__(self):
        return "sech(x)"
        
        
class CscH(Term):
    
    def generatePoint(self,x):
        try:
            return (x, 1/math.sinh(x))
        except:
            return None
            
    def deriv(self):
        return Product(Decimal(-1), CotH(), CscH())
        
    def  __repr__(self):
        return "csch(x)"
        
class CotH(Term):
    
    def generatePoint(self,x):
        try:
            return (x, 1/math.tanh(x))
        except:
            return None
            
    def deriv(self):
        return Sum (Decimal(1), Product(Decimal(-1), \
        Composition(CotH(), Power(2))))
        
    def  __repr__(self):
        return "coth(x)"
        


class Id(Term):
    
    def generatePoint(self,x):
        return (x,x)
        
    def deriv(self):
        return Decimal(1)

    def __repr__(self):
        return "x"
        
    def __eq__(self, other):
        return type(other) == Id

        


class Axes(object):
    
    def __init__(self,xMin = -10, xMax = 10, yMin = -10, yMax = 10, \
    xScale = 1, yScale = 1):
    
            
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax
        self.xScale = xScale
        self.yScale = yScale
        self.setVisualScales()
        
    def setVisualScales(self):
        
        domain = self.xMax - self.xMin
        tics = domain/self.xScale
        
        
        visualXScale = self.xScale
        if tics > 20:
            while tics > 20:
                visualXScale += self.xScale
                tics = domain/visualXScale
        elif tics < 3:
            while tics < 3:
                visualXScale /=10
                tics = domain/visualXScale
                
        self.visualXScale = visualXScale
        
        range = self.yMax - self.yMin
        tics = range/self.yScale
        
        visualYScale = self.yScale
        if tics > 20:
            while tics > 20:
                visualYScale += self.yScale
                tics = range/visualYScale
        elif tics < 3:
            while tics < 3:
                visualYScale /=10
                tics = range/visualYScale
                
        self.visualYScale = visualYScale
                
    
    def calculateOrigin (self, winWidth, winHeight):
        x = -self.xMin/(self.xMax - self.xMin)*winWidth
        y = self.yMax/(self.yMax - self.yMin)*winHeight
        return (x,y)
    
        
    def draw (self, canvas, winWidth, winHeight):
        
        origin = self.calculateOrigin(winWidth, winHeight)
        x0 = origin[0]
        y0 = origin[1]
        gray = '#%02x%02x%02x' % (169,169,169)
        
        
        x = x0 
        y = 0
        count = 0
        incrementX = self.visualXScale/(self.xMax - self.xMin)*winWidth
        
        while x < winWidth:
            
            canvas.create_line(x,y,x,y+winHeight, \
            fill =  gray)
            
            if count != 0:
                number = self.visualXScale*count
                
                if type(number) == float and len(str(number)) > 3:
                    number = float("%0.2f" % number)
                    
                if self.yMax < 0:
                    canvas.create_text(x, 1, text = str(number), anchor = N)
                elif self.yMin > 0:
                    canvas.create_text(x, winHeight, text = str(number), \
                    anchor = S)
                    
                else:
                    canvas.create_text(x, y0 + 1, text = str(number), \
                    anchor = N)
                    
                
                
            x += incrementX
            count += 1
        
        count = 0
        x = x0
        y = 0
        
        while x > 0:
            canvas.create_line(x,y,x,y+winHeight,\
            fill =  gray)
            
            if count != 0:
                
                number = self.visualXScale*count
                if type(number) == float and len(str(number)) > 3:
                    number = float("%0.2f" % number)
                    
                if self.yMax < 0:
                    canvas.create_text(x, 1, text = str(number), anchor = N)
                elif self.yMin > 0:
                    canvas.create_text(x, winHeight, text = str(number), \
                    anchor = S)
                    
                else:
                    canvas.create_text(x, y0 + 1, text = str(number), \
                    anchor = N)
                
            x -= incrementX
            count -= 1
          
        count = 0
        x = 0
        y = y0
        incrementY = self.visualYScale/(self.yMax - self.yMin)*winHeight
        
        while y > 0:
            canvas.create_line(x,y,x+winWidth,y, \
            fill =  gray)
            
            if count != 0:
                number = self.visualYScale*count
                if type(number) == float and len(str(number)) > 4:
                    number = float("%0.3f" % number)
                    
                if self.xMin >  0:
                    canvas.create_text(1, y, text = str(number), anchor = W)
                elif self.xMax  < 0:
                    canvas.create_text(winWidth, y, text = str(number), \
                    anchor = E)
                    
                else:
                    canvas.create_text(x0 +3, y, text = str(number), \
                    anchor = W)
                
                
                
            y -= incrementY
            count += 1
        
        count = 0
        x = 0
        y = y0
        while y < winHeight:
            canvas.create_line(x,y,x+winWidth,y, \
            fill =  gray)
            
            if count != 0:
                number = self.visualYScale*count
                
                if type(number) == float and len(str(number)) > 4:
                    number = float("%0.3f" % number)
                    
                if self.xMin >  0:
                    canvas.create_text(1, y, text = str(number), anchor = W)
                elif self.xMax  < 0:
                    canvas.create_text(winWidth, y, text = str(number), \
                    anchor = E)
                    
                else:
                    canvas.create_text(x0 +3, y, text = str(number), \
                    anchor = W)
                    
                
                
            y += incrementY
            count -= 1
        
        canvas.create_line(0, y0, winWidth, y0, width = 3)
        canvas.create_line(x0, 0, x0, winHeight, width = 3)
        
    def rescale(self, factor):
        domain = (self.xMax - self.xMin)
        cx = (self.xMax + self.xMin)/2
        range = (self.yMax - self.yMin)
        cy = (self.yMax + self.yMin)/2
        
        self.xMin = cx - (domain/2)*factor
        self.xMax = cx + (domain/2)*factor
        self.yMin = cy - (range/2)*factor
        self.yMax = cy + (range/2)*factor
        self.setVisualScales()
        
    def __repr__(self):
        return "(%0.2f, %0.2f,%0.2f,%0.2f,%0.2f,%0.2f,)" %\
        (self.xMin, self.xMax, self.yMin, self.yMax, self.xScale, self.yScale)
    

class Function (Term):
    
    def __init__(self, *args):
        
        self.color = "Black"
        self.terms = []
            
        if isinstance(args[0], list) and len(args) == 1:
            for term in args[0]:
                self.terms.append(term) 
            
        else:
            for term in args:
                
                self.terms.append(term)
        
            
            
    def setColor (self, color):
        self.color = color
        
    @abstractmethod
    def generatePoint(self, x):
        pass
        
    @abstractmethod
    def deriv(self):
        pass
        
    
    def draw (self, canvas, axes, winWidth, winHeight):
        
        totalPoints = 2000
        deltaX = (axes.xMax-axes.xMin)/totalPoints
        
        mathPoints = self.generatePoints(deltaX, axes)
        
        
        points = convertPoints(mathPoints, axes, \
        winWidth, winHeight)
        
        lines = []
        for i in range(len(points)-1):
            
            if isValidMidpoint(self, mathPoints[i], \
            mathPoints[i+1], axes, winWidth, winHeight):
                line = canvas.create_line(points[i], \
                points[i+1], fill = self.color,width = 3)
                lines.append(line)
        return lines
        
    
        
    def generatePoints(self, deltaX, axes):
        
        points = []
        
        x = axes.xMin
        while x <= axes.xMax:
            point = self.generatePoint(x)
            
            if point != None and type(point[1]) != complex:
                points.append(point)
            x += deltaX
        
        return points
            
        
   
        
class Sum (Function):#remove all zeros

    def __init__(self, *args):
        
        self.color = "blue"
        self.terms = []
        constant = 0
        
        if isinstance(args[0], list) and len(args) == 1:
            
            for term in args[0]:
                s = str(term).replace(" ", "")
                if not (s == "0" or s == "(0)"):
                    
                    if isinstance(term, Decimal):
                        constant += term.value
                    else:
                        self.terms.append(term) 
        
        else:
            for term in args:
                
                s = str(term).replace(" ", "")
                if not (s == "0" or s == "(0)"):
                
                    if isinstance(term, Decimal):
                        constant += term.value
                    else:
                        self.terms.append(term) 
       
        if not almostEqual(constant, 0):
            self.terms.append(Decimal(constant))
            
        if self.terms == []:
            self.terms = [Decimal(0)]
   
    def generatePoint(self, x):
        try:
            sum = 0
            for term in self.terms:
                sum += term.generatePoint(x)[1]
            return (x,sum)
        except:
            return None
        
    def deriv(self):
        derivTerms = []
        for term in self.terms:
            derivTerms.append(term.deriv())
        return Sum(derivTerms)
        
    def __repr__(self):
        s = ''
        for term in self.terms:
            '''
            if str(term).replace(" ","")[0] == "-":
                print(s)
                s = s[:-2] 
                
            '''
            
            
            s += "%s + " % str(term)
        return s[:-2]
        
class Product (Function):#remove all ones
    
    def __init__(self, *args):
        
        
        if not list(args) == [Decimal(1)] :
            self.terms = []
            constant = 1
            
            if isinstance(args[0], list) and len(args) == 1:
                #print(args[0])
                for term in args[0]:
                    
                    s = str(term).replace(" ", "")

                    
                    if s == "0" or s == "(0)":
                        self.terms = [Decimal(0)]
                        return None
                        
                    elif not (s == "1" or s == "(1)"):
                        if isinstance(term, Decimal):
                            constant *= term.value
                        
                        else:
                            self.terms.append(term) 
            
            
            else:
                #print(args)
                for term in args:
                    
                    s = str(term).replace(" ", "")

                    
                    if s == "0" or s == "(0)":
                        self.terms = [Decimal(0)]
                        return None
                        
                    elif not (s == "1" or s == "(1)"):
                        if isinstance(term, Decimal):
                            constant *= term.value
                        
                        else:
                            self.terms.append(term) 
                    
            if not almostEqual(constant, 1):
                self.terms.insert(0, Decimal(constant))
        else:
            self.terms = [Decimal(1)]
        
    def generatePoint(self,x):
        try:
            product = 1
            for term in self.terms:
                product *= term.generatePoint(x)[1]
            return (x,product)
        except:
            return None
        
    def deriv(self):
        #print(self)
        terms = copy.deepcopy(self.terms)
        lastTerm = terms.pop()
        firstTerms = Product(terms)
        
        if len(self.terms) == 1:
            return self.terms[0].deriv()
            
        else:
            
            aPrimeB = Product(firstTerms.deriv(), lastTerm)
            bPrimeA = Product (firstTerms, lastTerm.deriv())
            return Sum(aPrimeB, bPrimeA)
        
        
    def __repr__(self):
        s = ""
        i = 0
        while i < (len(self.terms)): 
            term = self.terms[i]
            '''
            if term == Decimal(-1) and i != len(self.terms)-1:
                term = self.terms[i + 1]
                i +=2
                if str(term)[0] == "-":
                    s += "(%s) * " % str(term)[1:]
                else:
                    s += "(-%s) * " % str(term)
            '''
            if type(term) in [Sum, Fraction, HyperPower, Power, Exponent]:
                s += "(%s) * " % str(term)
                i += 1
            else:
                s += "%s * " % str(term)
                i += 1
                
        return s[:-2]
        
        


class Fraction (Function):
    
    def generatePoint(self,x):
        try:
            num = self.terms[0]
            denom = self.terms[1]
            y = num.generatePoint(x)[1]/denom.generatePoint(x)[1]
            return (x,y)
        except:
            return None
        
        
    def deriv(self):
        denom = self.terms[1]
        num = self.terms[0]
        loDhi = Product(denom, num.deriv())
        hiDlo = Product(Decimal(-1), num, denom.deriv())
        lolo = Composition(denom, Power(2))
        return Fraction(Sum(loDhi,hiDlo),lolo)
        
    #clean up fractions by checking for same terms 
    def __repr__(self):
        
        denom = str(self.terms[1]).replace(" ", "")
        num = str(self.terms[0]).replace(" ", "")
        
        
        if denom == "1" or denom == "(1)":
            return "%s" % num
            
        if num == "0" or num == "(0)":
            return "0"
            
        
        if type(self.terms[0]) in [Sum, Product, HyperPower, Power, \
        Exponent, NaturalExpo]:
            num = "(%s)" % num
            
        if type(self.terms[1]) in [Sum, Product, HyperPower, Power, \
        Exponent, NaturalExpo]:
            denom = "(%s)" % denom
        
        return "%s/%s" % (num, denom)
    
    def generatePoint(self,x):
        try:
            num = self.terms[0]
            denom = self.terms[1]
            y = num.generatePoint(x)[1]/denom.generatePoint(x)[1]
            return (x,y)
        except:
            return None
        
        
    def deriv(self):
        denom = self.terms[1]
        num = self.terms[0]
        loDhi = Product(denom, num.deriv())
        hiDlo = Product(Decimal(-1), num, denom.deriv())
        lolo = Composition(denom, Power(2))
        return Fraction(Sum(loDhi,hiDlo),lolo)
        
    #clean up fractions by checking for same terms 
    def __repr__(self):
        
        denom = str(self.terms[1]).replace(" ", "")
        num = str(self.terms[0]).replace(" ", "")
        
        
        if denom == "1" or denom == "(1)":
            return "%s" % num
            
        if num == "0" or num == "(0)":
            return "0"
            
        
        if type(self.terms[0]) in [Sum, Product, HyperPower, Power, \
        Exponent, NaturalExpo]:
            num = "(%s)" % num
            
        if type(self.terms[1]) in [Sum, Product, HyperPower, Power, \
        Exponent, NaturalExpo]:
            denom = "(%s)" % denom
        
        return "%s/%s" % (num, denom)
         
class HyperPower(Function):
    
    def generatePoint(self,x):
        try:
            base = self.terms[0].generatePoint(x)[1]
            expo = self.terms[1].generatePoint(x)[1]
            return (x, base**expo)
        except:
            return None
        
    def deriv(self):
        base = self.terms[0]
        expo = self.terms[1]
        term1 = HyperPower(self.terms)
        miniTerm1 = Product(expo.deriv(), Composition(base, NaturalLog()))
        miniTerm2 = Fraction(Product(expo, base.deriv()), base)
        term2 = Sum (miniTerm1, miniTerm2)
        return Product(term1, term2)
        
    def __repr__(self):
        base = str(self.terms[0])
        expo = str(self.terms[1])
        
        return "(%s)^(%s)" %(base, expo)
        

class Composition(Function):
    
    def __init__(self, *args):
        
        self.terms = []
            
        if isinstance(args[0], list) and len(args) == 1:
            for term in args[0]:
                self.terms.append(term) 
            
        else:
            for term in args:
                self.terms.append(term)
        
        if isinstance(self.terms[0], Id):
            self.terms.pop(0)
        
    def generatePoint(self, x):
        try:
            y = x
            for term in self.terms:
                y = term.generatePoint(y)[1]
            return (x,y)
        except:
            return None
        
    def deriv(self):
        terms = copy.deepcopy(self.terms)
        derivTerms = []
        for i in range (len(terms)):
            lastterm = terms.pop()
            terms.append(lastterm.deriv())
            derivTerms += [Composition(terms)]
            terms.pop()
        return Product(derivTerms)
        
        
    def __repr__(self):
        terms = copy.deepcopy(self.terms)
        s = str(terms.pop())
        while len(terms) > 0:
            term = terms.pop()
            if type(term) in [Sum, Product, HyperPower, Composition]:
                s = s.replace('x', "(" + str(term) + ")")
            else:
                s = s.replace('x', str(term))
        return s
    
class Polar(Function):
    
    def __init__(self, function, thetaMin = 0, thetaMax = 6.28, \
    thetaStep = 0.01):
        self.function = function
        self.thetaMin = thetaMin
        self.thetaMax = thetaMax
        self.thetaStep = thetaStep
        self.color = "blue"
        
    def deriv(self):
        pass
        
    def generatePoint(self,x):
        try:
            theta = x
            r = self.function.generatePoint(x)[1]
            return (r*math.cos(x), r*math.sin(x))
        except:
            return None
        
    def draw (self, canvas, axes, winWidth, winHeight):
        
        totalPoints = 2000
        deltaX = (axes.xMax-axes.xMin)/totalPoints
        
        mathPoints = self.generatePoints(deltaX, axes)
        
        
        points = convertPoints(mathPoints, axes, \
        winWidth, winHeight)
        
        for i in range(len(points)-1):
            
            canvas.create_line(points[i], points[i+1], fill = self.color, \
            width = 3)
        
    def generatePoints(self, dx, axes):
        
        points = []
        
        theta = self.thetaMin
        while theta <= self.thetaMax:
            point = self.generatePoint(theta)
            if point != None and type(point[1]) != complex:
                points.append(point)
            theta += self.thetaStep
        return points
        
    def __repr__ (self):
        return str(self.function).replace('x',  u"\u03F4")
    
class Parametric(Function):
    
    def __init__(self, functionX, functionY, tMin=0, tMax=10):
        self.functionX = functionX
        self.functionY = functionY
        self.tMin = tMin
        self.tMax = tMax
        self.color = "red"
        
    def deriv(self):
        pass
        
    def generatePoint(self,x):
        try:
            pX = self.functionX.generatePoint(x)[1]
            pY = self.functionY.generatePoint(x)[1]
            return (pX,pY)
        except:
            return None
        
    def generatePoints(self, dx, axes):
        
        points = []
        tStep = (self.tMax-self.tMin)/2000
        
        t = self.tMin
        while t <= self.tMax:
            point = self.generatePoint(t)
            if point != None and type(point[1]) != complex:
                points.append(point)
            t += tStep
        return points
        
    def alterTMax(self, dt):
        self.tMax += dt
        
    def __repr__ (self):
        return str(self.functionX).replace('x',  't') + ',' + \
        str(self.functionY).replace('x',  't')
        
    def functionXtoString(self):
        return str(self.functionX).replace('x',  't')
    
    def functionYtoString(self):
        return str(self.functionY).replace('x',  't')
    
    def draw (self, canvas, axes, winWidth, winHeight):
        
        totalPoints = 2000
        deltaX = (axes.xMax-axes.xMin)/totalPoints
        
        mathPoints = self.generatePoints(deltaX, axes)
        
        
        points = convertPoints(mathPoints, axes, \
        winWidth, winHeight)
        
        for i in range(len(points)-1):
            
            canvas.create_line(points[i], points[i+1], fill = self.color, \
            width = 3)
    
    
def parseFunction (function, var, center = 0):
    
    #print("this is the parsefunction")
    function = function.replace(" ", "")
    #print(function)
    functions = []
    operations =[]
    
    index = 0
    while index < len(function):
        char = function[index]
        #print(functions, operations)
                
        if ( isImpliedMultiplication(function, index)):
            operations.append("*")
            
        
        if (char == '('):
        
            #modify helper function for (|[
            nestedFunction = isolateInnerFunction(function, index, '(')

            innerFunction = parseFunction (nestedFunction, var)
            functions.append(innerFunction)
            
            index += (len(nestedFunction) + 2)
            
        
        
        elif (char == '['):
        
            nestedFunction = isolateInnerFunction(function, index, '[')

            innerFunction = parseFunction (nestedFunction, var)
            functions.append(Composition (innerFunction, Floor()))
            
            index += (len(nestedFunction) + 2)

        
        
        elif (char == '|'):
        
            absVal = isolateAbsValTerm(function, index)
            
            innerFunction = parseFunction (absVal, var)
            absValTerm = Composition (innerFunction, Abs())
            functions.append(absValTerm)
            
            index += (len(absVal)+2)
        
       
        elif (char in "-*+/^"):
        
            if (isUnaryOperator(function, index)):
            
                negative = Decimal(-1)
                functions.append(negative)
                operations.append("*")
                index += 1
            
            else:
            
                operation = char
                operations.append(operation)
                index += 1
            
        
        
        
        
        elif  char.isalpha() :
        
            if (char == var or char == var.upper()):
            
                term = Id()
                index += 1
                functions.append(term)
            
            elif (char == 'e'):
            
                term = Decimal(math.e)
                index += 1
                functions.append(term)
                
            elif (char == u"\u03C0"):
                
                term = Decimal(math.pi)
                index += 1
                functions.append(term)
                
            elif (function[index:index+4]==  "d/dx" ):
            
                
                index += 4
                
                nestedFunction = isolateInnerFunction (function, index, '(')
                innerFunction = parseFunction (nestedFunction, var)
                der = innerFunction.deriv()
                functions.append(der)
                
                index += (len(nestedFunction) + 2)
            
            else:
            
                substring = function[index:]
                tuple = parseTerm(substring)
                term = tuple[0]
                index += tuple[1]
                
                nestedFunction = isolateInnerFunction (function, index, '(')
                innerFunction = parseFunction (nestedFunction, var)
                composition = Composition(innerFunction, term)
                functions.append(composition)
                
                index += (len(nestedFunction) + 2)		
                
            
        
        elif (char.isdigit()):
        
            coeff = isolateDouble(function, index)
            #print("coeff =" + coeff)
            decimal = Decimal (float(coeff))
            #print("decimal = " + str(decimal))
            functions.append(decimal)
            
            index += len(coeff)
        
        elif (char == u"\u222B"):
            
            index += 1
            nestedFunction = isolateInnerFunction(function, index, '(')
            innerFunction = parseFunction (nestedFunction, var)
            integral = integralTaylorApproximation(innerFunction, 17, center)
            functions.append(integral)
            
            index += len(nestedFunction) + 4
            
        else:
            raise Exception('invalid string characters contained')
    #print(functions, operations)
    return pemdas(functions, operations)
    


def parseTerm (term):
 
    term += "------"
    function = None
    index = 0
    stringLength = 0 
    
    if (term[index:index+4] =="sinh"):
    
        function = SinH()
        stringLength = 4
    
    elif (term[index:index+4] =="cosh"):
     
        function = CosH() 
        stringLength = 4
     
    elif (term[index:index+4] =="tanh"):
     
        function = TanH() 
        stringLength = 4
     
    elif (term[index:index+4] =="sech"):
     
        function = SecH() 
        stringLength = 4
     
    elif (term[index:index+4] =="coth"):
     
        function = CotH() 
        stringLength = 4
     
    elif (term[index:index+4] =="csch"):
     
        function =  CscH() 
        stringLength = 4
        
    
    elif (term[index:index+3] =="sin"):
     
        function =  Sin() 
        stringLength = 3
     
    elif (term[index:index+3] =="cos"):
     
        function =  Cos() 
        stringLength = 3
     
    elif (term[index:index+3] =="tan"):
     
        function = Tan() 
        stringLength = 3
     
    elif (term[index:index+3] =="csc"):
     
        function = Csc() 
        stringLength = 3
     
    elif (term[index:index+3] =="sec"):
     
        function =  Sec() 
        stringLength = 3
     
    elif (term[index:index+3] =="cot"):
     
        function =  Cot() 
        stringLength = 3
     
    elif (term[index:index+6] =="arcsin"):
     
        function =  ArcSin()
        stringLength = 6 
     
    elif (term[index:index+6] =="arccos"):
     
        function =  ArcCos() 
        stringLength = 6 
     
    elif (term[index:index+6] =="arctan"):
     
        function =  ArcTan() 
        stringLength = 6 
     
    elif (term[index:index+6] =="arccot"):
     
        function =  ArcCot() 
        stringLength = 6  
     
    elif (term[index:index+6] =="arccsc"):
     
        function =  ArcCsc() 
        stringLength = 6 
     
    elif (term[index:index+6] =="arcsec"):
     
        function =   ArcSec()
        stringLength = 6  
     
    elif (term[index:index+3] =="log"):
     
        function =   Log() 
        stringLength = 3
     
    elif (term[index:index+2] =="ln"):
     
        function =  NaturalLog() 
        stringLength = 2 
    else:
        return None
    return (function, stringLength)
 

def pemdas (functions, operations):
 
    i = 0
    while i < len(operations):
        
        if (operations[i]=="^"):
         
            #print("^", functions, operations)
            if (isinstance(functions[i],Decimal)):
                if type(functions[i+1]) == Id:
                    
                    composition = Exponent(functions[i].value)
                    #print(functions[i].value)
                else:
             
                    base = functions[i].value 
                    expo = Exponent (base) 
                    composition =  Composition (functions[i+1], expo) 
                functions.pop(i+1) 
                functions[i]= composition
                operations.pop(i) 
                i -= 1
             
            elif (isinstance(functions[i+1],Decimal)):
             
                pow = functions[i+1].value  
                powerTerm =  Power (pow) 
                functions.pop(i+1) 
                
                if functions[i] == Id():
                    functions[i] = powerTerm
                else:
                    composition =   Composition (functions[i], powerTerm) 
                    functions[i] = composition
                
                operations.pop(i) 
                i -= 1
             
            else:
             
                hyperPower =   HyperPower( functions[i], functions[i+1]) 
                functions.pop(i+1) 
                functions[i] =  hyperPower
                operations.pop(i) 
                i -= 1
            #print("^", functions, operations)
            
        i += 1
    
    i = 0
    while i < len(operations):
     
        if (operations[i] == "*"):
         
            product =   Product ( functions[i],  functions[i+1]) 
            functions.pop(i+1) 
            functions[i]= product
            operations.pop(i) 
            i -= 1
        
            #print("*", functions, operations)

        i += 1
         
    i = 0
    while i < len(operations):
     
        if (operations[i] == "/"):
         
            quotient =  Fraction ( functions[i],  functions[i+1]) 
            functions.pop(i+1) 
            functions[i] =  quotient
            operations.pop(i) 
            i -= 1


        i += 1
        
    i = 0
    while i < len(operations):
     
        if (operations[i] == "-"):
         
            difference =  Sum(functions[i],Product(Decimal(-1),functions[i+1])) 
            functions.pop(i+1) 
            functions[i] =  difference
            operations.pop(i) 
            i -= 1


        i += 1
         
    i = 0
    while i < len(operations):
     
        if (operations[i] == "+"):
         
            sum =  Sum ( functions[i],  functions[i+1]) 
            functions.pop(i+1) 
            functions[i] =  sum
            operations.pop(i) 
            i -= 1
           
        i += 1
   
    return  functions[0]
 

def isUnaryOperator( function,  index):
 
    char  = function[index] 
    if (char == '-'):
     
        if (index == 0):
         
            return True 
         
        else:
            previousChar = function[index-1]
            if (previousChar in "-*+/^"):
                return True 
             
    return False 
    
 

def isolateInnerFunction(function, index, openVar):
    
    closeVar = ""
    if openVar == "(":
        closeVar = ")"
    elif openVar == "[":
        closeVar = "]"
    
    closedBracketFinder = index + 1 
    openParenthCounter = 0 
    closedParenthCounter = 0 
    
    done = closedParenthCounter == openParenthCounter + 1 
    while (not done):
        #print(function[closedBracketFinder] )
        if (function[closedBracketFinder] == closeVar):
            closedParenthCounter += 1 
            
        if (function[closedBracketFinder] == openVar):
            openParenthCounter += 1  
        
        closedBracketFinder += 1  
        
        if( closedParenthCounter == openParenthCounter + 1):
            
            done = True 
            closedBracketFinder -= 1
            
        
         
        
        
    nestedFunction = function[index + 1: closedBracketFinder]
    return nestedFunction 
 



def isolateDouble ( function,  index):
    
    coeff = float(function[index])
    number = "" 
    i = index + 2
    while (True):
        
        if i > len(function) + 1:
            number = function[index: i] 
            break
        try:
         
            number = function[index: i]
            coeff = float(number) 
            i += 1
         
        except: 
            
            i -= 1
            number = function[index: i] 
            
            break 
            
        
    
    return number 
 

def isImpliedMultiplication ( function, index):
 
    
        if (index < 1):
            return False 

        return function[index-1] not in "-*+/^" and \
        function[index] not in "-*+/^"  
            
 

def isolateAbsValTerm ( function,  index):
 
    delimitFinder = index + 1 
    
    done = False 
    while (not done):
     
        char = function[delimitFinder]
        
        if (char == '|'):
            done = True 
        elif (char == '('):
         
            inner = isolateInnerFunction(function, delimitFinder, '(') 
            delimitFinder += len(inner) + 2 
         
        elif (char == '['):
         
            inner = isolateInnerFunction(function, delimitFinder, '[') 
            delimitFinder += len(inner) + 2 
            
        else:
            delimitFinder+=1
     
    
    return function[index + 1: delimitFinder]
 
def convertXInverse(xP, axes, winWidth, winHeight):
    
    origin = axes.calculateOrigin(winWidth, winHeight)
    x0 = origin[0]
    domain = axes.xMax - axes.xMin
    
    x = (xP-x0)*domain/winWidth
    
    return x
    
def convertPointInverse(point, axes, winWidth, winHeight):
    xP = point[0]
    yP = point[1]

    origin = axes.calculateOrigin(winWidth, winHeight)
    x0 = origin[0]
    y0 = origin [1]
    domain = axes.xMax - axes.xMin
    range = axes.yMax - axes.yMin
    
    x = (xP-x0)*domain/winWidth
    y = (y0-yP)*range/winHeight
    
    return (x,y)
    
def convertPoint(point, axes, winWidth, winHeight):
    
    origin = axes.calculateOrigin(winWidth, winHeight)
    x0 = origin[0]
    y0 = origin [1]
    domain = axes.xMax - axes.xMin
    range = axes.yMax - axes.yMin
    
    x = x0 + point[0]/domain*winWidth
    y = y0 - point[1]/range*winHeight
    
    return (x,y)
    
def convertPoints(points, axes, winWidth, winHeight):
    
    newPoints = []
    for point in points:
        newPoints.append(convertPoint(point,axes, winWidth, winHeight))
    return newPoints
    
def nthDeriv(function, n):
    if n < 0:
        n = 0
    d = function
    while n > 0:
        d = d.deriv()
        n -= 1
    return d
    
    
def appendTaylorTerm(function, i, center, terms):
    deriv = nthDeriv(function, i).generatePoint(center)[1]
    cn = Fraction(Decimal(deriv), Decimal(math.factorial(i+1)) )
    power = Composition(Sum(Id(), Decimal(-center)), Power(i+1))
    terms.append(Product(cn, power))
        
    

def integralTaylorApproximation(function, degree, center):
    
    if degree < 0:
        degree = 0
    terms = []
    #for i in range(degree+1):
        #print(i)
        #print(i)
    pool = mp.Pool(processes = 8)
    
    reuslts = [pool.apply_async(appendTaylorTerm, args = (function, i , \
    center, terms)) for i in range (degree+1)]    
        
    return Sum(terms)
    
def instantaneousSlope(function, x):
    h = 10**-7
    dy = function.generatePoint(x+h)[1] - function.generatePoint(x+h)[0]
    dx = h
    return dy/dx
    

    
def callWithLargeStack(f,*args):
    import sys
    import threading
    threading.stack_size(2**27)  # 64MB stack
    sys.setrecursionlimit(2**27) # will hit 64MB stack limit first
    # need new thread to get the redefined stack size
    def wrappedFn(resultWrapper): resultWrapper[0] = f(*args)
    resultWrapper = [None]
    #thread = threading.Thread(target=f, args=args)
    thread = threading.Thread(target=wrappedFn, args=[resultWrapper])
    thread.start()
    thread.join()
    return resultWrapper[0]
    
def isValidMidpoint(function, point1, point2, axes, winWidth, winHeight):
    
    
    xBar = (point1[0] + point2[0])/2
    yBar = (point1[1] + point2[1])/2
    y = function.generatePoint(xBar)[1]
    
    yBarPrime = convertPoint((xBar,yBar), axes, winWidth, winHeight)[1]
    yPrime = convertPoint((xBar,y), axes, winWidth, winHeight)[1]
    d = abs(yBarPrime-yPrime)
    range = axes.yMax - axes.yMin
    
    validMidpoint = d/range < 0.2
    
    
    return validMidpoint 
    
def printTerms(function):
    
    if type(function) not in [Sum, Product, Fraction, HyperPower]:
        print(function, end = '  ')
        print(type(function), end = '  ')
    else:
        for term in function.terms:
            printTerms(term)
            

def findIntersections(function1, function2, xMin, xMax):
    Difference = Sum(function1, Product(Decimal(-1), function2))
    derivative = Difference.deriv()
    
    
    intersections = newtonsApproximation(Difference, derivative, xMin, xMax,[])
    removeDuplicates(intersections)
    
    #print(intersections)
    points = []
    for x in intersections:
       
        y = function1.generatePoint(x)[1]
        
        if almostEqual(x%1, 0, (xMax - xMin)/100000):
            x = roundHalfUp(x)
            
        elif type(x) == float and len(str(x)) > 4:
            x = float("%0.3f" % x)
        
        if almostEqual(y%1, 0, (xMax - xMin)/100000):
            y = roundHalfUp(y) 
            
        elif type(y) == float and len(str(y)) > 4:
            y = float("%0.3f" % y)
            
        
        points.append((x,y))

    return points
    
def findAllIntersections (functions, xMin, xMax):
    points = []
    for i in range (len(functions)-1):
        for j in range(i, len(functions)):
            intersections = findIntersections(functions[i], functions[j], \
            xMin, xMax)
            for point in intersections:
                if point not in points:
                    points.append(point)
                    
    return points
    
def removeDuplicates(l):
    #print(l)
    i = 0
    while i < (len(l)):
        j = i
        while j < len(l):
            if l[i] == l[j] and i != j:
                l.pop(j)
                j -= 1
            j += 1
        i += 1
    
    #print(l)
    
    
def newtonsApproximation(difference, derivative, xMin, xMax, intersections):
    
    
    #print(xMin, xMax)
    startingGuesses = createStartingGuesses(xMin, xMax)
    guessIndex = 0
    guess = startingGuesses[guessIndex] 
    
    domain = xMax - xMin
    guessFound = False
    count = 0
    maxCount = 20
    
    #print("difference %s" % difference, "derivative %s" %derivative)
    while not guessFound:
        #print(guessIndex)
        
        try:
            newGuess = (guess - 
            difference.generatePoint(guess)[1]/ \
            (derivative.generatePoint(guess)[1]))
            
            if newGuess>xMax:
                newGuess = guess - 0.1*domain
            elif newGuess<xMin:
                newGuess = guess + 0.1*domain
                
            #print("ng", newGuess)
            #print(difference.terms)
    
            if almostEqual(difference.generatePoint(newGuess)[1], 0, 10**-9):
                guessFound = True
            elif count >maxCount:
                guessIndex+=1
                if guessIndex < len(startingGuesses):
                    newGuess = startingGuesses[guessIndex]
                    
                    count = 0
                else:
                    break
                
            guess = newGuess
            count += 1
            
        except:
            guessIndex+=1
            if guessIndex < len(startingGuesses):
                newGuess = startingGuesses[guessIndex]
                count = 0
            else:
                break
            guess = newGuess
            count += 1
        
    #print(xMin, xMax, intersections)
    if guessFound:
        domain = xMax - xMin
        margin = domain/1000
        
        return [guess] + (newtonsApproximation(difference, derivative, \
        xMin, guess-margin, intersections) +newtonsApproximation(difference, \
        derivative, guess+margin, xMax, intersections))
    else:
        return []
        
#if user clicks on the intersections then display the coordinates of the point
#this can be applied to regression when user clicks on a dot
def drawPoints(points, canvas, axes, winWidth, winHeight, color = "red"):
    
    #print(intersections)
    
    graphicsPoints = convertPoints(points, axes, winWidth, winHeight)
    for i in range(len(graphicsPoints)):
        point = graphicsPoints[i]
        cx = point[0]
        cy = point[1]
        r = 5
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = color, width = 0)
        
        xVal = points[i][0]
        yVal = points[i][1]
        
        #labelPoint(canvas, cx, cy, xVal, yVal,r)
        

        
def labelPoint (canvas, cx, cy, xVal, yVal,r):
    canvas.create_text(cx-r, cy-r, text = "(" + str(xVal)+ ","+ \
    str(yVal) +")", anchor = SE, font = "Times ")
    
        
def createStartingGuesses(xMin, xMax):
    startingGuesses = []
    first = (xMin + xMax)/2
    startingGuesses += [first]
    
    domain = xMax - xMin
    increment = domain/10
    
    guess = first + increment
    while guess < xMax:
        startingGuesses.append(guess)
        guess += increment
        
    guess = first - increment
    while guess > xMin:
        startingGuesses.append(guess)
        guess -= increment
        
    #print(startingGuesses)
    return startingGuesses
    
        
def findXIntercepts(function, xMin, xMax):
    function2 = Decimal(0)
    return findIntersections(function, function2, xMin, xMax)
    
def findYIntercept(function):
    point = function.generatePoint(0)
    if point != None:
        return [function.generatePoint(0)]
    return []
    
def findXYIntercepts(function, xMin, xMax):
    
    intercepts = []
    intercepts += findXIntercepts(function, xMin, xMax)
    intercepts += findYIntercept(function)
    return intercepts
    
def findfAllIntercepts(functions, xMin, xMax):
    intercepts = []
    for function in functions:
        points = findXYIntercepts(function, xMin, xMax)
        for point in points:
            if point not in intercepts:
                intercepts += [point]
    return intercepts
        
def findAllImportantPoint (functions, xMin, xMax):
    points = []
    points += findAllIntersections(functions, xMin, xMax)
    intercepts = findfAllIntercepts(functions, xMin, xMax)
    for intercept in intercepts:
        if intercept not in points:
            points += [intercept]
    return points
    
def drawXIntercepts (xIntercepts, canvas, axes, winWidth, winHeight, \
color = "red"):
    drawPoints(xIntercepts, canvas, axes, winWidth, winHeight, color )
    
def parseValue (function):
    
    function = function.replace(" ", "")
    functions = []
    operations =[]
    
    index = 0
    while index < len(function):
        char = function[index]
       
                
        if ( isImpliedMultiplication(function, index)):
            operations.append("*")
            
        
        if (char == '('):
        
            
            nestedFunction = isolateInnerFunction(function, index, '(')

            innerFunction = parseValue (nestedFunction)
            functions.append(innerFunction)
            
            index += (len(nestedFunction) + 2)
            
        
        
        elif (char == '['):
        
            nestedFunction = isolateInnerFunction(function, index, '[')

            innerFunction = parseValue (nestedFunction)
            functions.append(Composition (innerFunction, Floor()))
            
            index += (len(nestedFunction) + 2)

        
        
        elif (char == '|'):
        
            absVal = isolateAbsValTerm(function, index)
            
            innerFunction = parseValue (absVal)
            absValTerm = Composition (innerFunction, Abs())
            functions.append(absValTerm)
            
            index += (len(absVal)+2)
        
       
        elif (char in "-*+/^"):
        
            if (isUnaryOperator(function, index)):
            
                negative = Decimal(-1)
                functions.append(negative)
                operations.append("*")
                index += 1
            
            else:
            
                operation = char
                operations.append(operation)
                index += 1
            
        
        
        
        
        elif  char.isalpha() :
        
            
            
            if (char == 'e'):
            
                term = Decimal(math.e)
                index += 1
                functions.append(term)
                
            elif (char == u"\u03C0"):
                
                term = Decimal(math.pi)
                index += 1
                functions.append(term)
                
            
            
            else:
            
                substring = function[index:]
                tuple = parseTerm(substring)
                term = tuple[0]
                index += tuple[1]
                
                nestedFunction = isolateInnerFunction (function, index, '(')
                innerFunction = parseValue (nestedFunction)
                composition = Composition(innerFunction, term)
                functions.append(composition)
                
                index += (len(nestedFunction) + 2)			
            
        
        elif (char.isdigit()):
        
            coeff = isolateDouble(function, index)
            #print("coeff =" + coeff)
            decimal = Decimal (float(coeff))
            #print("decimal = " + str(decimal))
            functions.append(decimal)
            
            index += len(coeff)
        
        elif (char == u"\u222B"):
            
            index += 1
            nestedFunction = isolateInnerFunction(function, index, '(')
            innerFunction = ParseValue (nestedFunction, var)
            integral = integralTaylorApproximation(innerFunction, 17, center)
            functions.append(integral)
            
            index += len(nestedFunction) + 4
            
    
    #print(functions, operations)
    return valuePemdas(functions, operations)
    
    
    
def valuePemdas (functions, operations):
 
    i = 0
    while i < len(operations):
        
        if (operations[i]=="^"):
         
            hyperPower =   HyperPower( functions[i], functions[i+1]) 
            functions.pop(i+1) 
            functions[i] =  hyperPower
            operations.pop(i) 
            i -= 1
            #print("^", functions, operations)
            
        i += 1
    
    i = 0
    while i < len(operations):
     
        if (operations[i] == "*"):
         
            product =   Product ( functions[i],  functions[i+1]) 
            functions.pop(i+1) 
            functions[i]= product
            operations.pop(i) 
            i -= 1
        
            #print("*", functions, operations)

        i += 1
         
    i = 0
    while i < len(operations):
     
        if (operations[i] == "/"):
         
            quotient =  Fraction ( functions[i],  functions[i+1]) 
            functions.pop(i+1) 
            functions[i] =  quotient
            operations.pop(i) 
            i -= 1


        i += 1
        
    i = 0
    while i < len(operations):
     
        if (operations[i] == "-"):
         
            difference =  Sum(functions[i],Product(Decimal(-1),functions[i+1])) 
            functions.pop(i+1) 
            functions[i] =  difference
            operations.pop(i) 
            i -= 1


        i += 1
         
    i = 0
    while i < len(operations):
     
        if (operations[i] == "+"):
         
            sum =  Sum ( functions[i],  functions[i+1]) 
            functions.pop(i+1) 
            functions[i] =  sum
            operations.pop(i) 
            i -= 1
            #print("+", functions, operations)

        i += 1
         
    #print("+", functions, operations)
    
         
    #print("pemdas " + str(functions[0]))
    return  functions[0]## is this enough ie when only 1 term?
    
def formatValue (value):
    if type(value) == int:
        return str(value)
    elif almostEqual(value%1, 0):
        return str(roundHalfUp(value))
    else:
        return "%0.3f"%value
        
def isNearIntersection(clickPoint, GUI):
    intersections = GUI.cartesianPoints
    x = clickPoint[0]
    y = clickPoint[1]
    domain = GUI.cartesianAxes.xMax - GUI.cartesianAxes.xMin
    range = GUI.cartesianAxes.yMax - GUI.cartesianAxes.yMin
    h = GUI.canvasHeight
    w = GUI.canvasWidth
    for point in intersections:
        graphicsPoint = convertPoint(point, GUI.cartesianAxes, \
        GUI.canvasWidth, GUI.canvasHeight)
        x1 = graphicsPoint[0]
        y1 = graphicsPoint[1]
        dx = x-x1
        dy = y-y1
        
        #print(( dx**2 + dy**2 )**0.5)
        if ( dx**2 + dy**2 )**0.5 < 10:
            return (True, point)
        
    return (False,None)
        
        

def parseStatsData(data):
    l = []
    data =data.replace(" ", "")
    data = data.replace("\n", "")
    index = 0
    while index < len(data):
        char = data[index]
        if char == "(":
            
            coordinate = isolateInnerFunction(data, index , '(')
            #print(coordinate)
            commaIndex = coordinate.find(",")
            #print(coordinate[:commaIndex])
            x = parseValue(coordinate[:commaIndex]).generatePoint(1)[1]
            x = float(formatValue(x))
            y = parseValue(coordinate[commaIndex+1:]).generatePoint(1)[1]
            y = float(formatValue(y))
            
            index += len(coordinate) + 2
            l.append((x,y))
        elif char == ",":
            index += 1
        else:
            raise Exception ('invalid string characters contained')
                
    return l
    
def isolateCoordinate(data, index):
    finder = index
    while data[finder] != ')':
        finder += 1
       
    #print(index, finder)
    return data[index + 1: finder]
    
def main():
        
    winWidth = 1000
    winHeight = 800
    root = Tk()
    canvas = Canvas(root, width=winWidth, height=winHeight)
    canvas.pack()
    
    axes = Axes(-10, 10, -10, 10, 1, 1)
    axes.draw(canvas, winWidth, winHeight)
    
    
    fp = Sum(parseFunction("arcsin(sin(4x))", 'x'))
    gp = Sum(Sec())
    gp.setColor("red")
    
    fp.draw(canvas, axes, winWidth, winHeight)
    gp.draw(canvas, axes, winWidth, winHeight)
    
    intersections = findIntersections(fp, gp, axes.xMin, axes.xMax)
    drawPoints(intersections, canvas, axes, winWidth, winHeight, "green")
    '''
    '''
    '''
    f = Sum(parseFunction("[x]", 'x'))
    g = Sum(Power(1.6))
    g.setColor("red")
    
    f.draw(canvas, axes, winWidth, winHeight)
    g.draw(canvas, axes, winWidth, winHeight)
    
    intersections = findIntersections(f, g, axes.xMin, axes.xMax)
    drawPoints(intersections, canvas, axes, winWidth, winHeight, "green")
    '''
    '''
    george = Sum(parseFunction("0.5",'x'))
    george.draw(canvas, axes, winWidth, winHeight)
    
    brittany = Sum(parseFunction("sin(x)",'x'))
    brittany.setColor("red")
    brittany.draw(canvas, axes, winWidth, winHeight)
    
    intersections = findIntersections(george, brittany, axes.xMin, axes.xMax)
    drawPoints(intersections, canvas, axes, winWidth, winHeight, "green")
    '''
    
    integral = u"\u222B"
    pi = u"\u03C0"
    theta = u"\u03F4"
    
    '''
    archana = Sum(parseFunction("sin(%sx)" %pi, 'x'))
    #archanaprime = Sum(parseFunction("x^3/3 -x^2 + 3x", 'x'))
    #archanaprime.setColor("green")
    archana.draw(canvas, axes, winWidth, winHeight)
    #archanaprime.draw(canvas, axes, winWidth, winHeight)
    '''
    '''
    ray = Sum(parseFunction("[x]", 'x'))
    ray.setColor("red")
    ray.draw(canvas, axes, winWidth, winHeight)
    
    intersections = findIntersections(archana, ray, axes.xMin, axes.xMax)
    drawPoints(intersections, canvas, axes, winWidth, winHeight, "green")
    '''
    #xInts = findXIntercepts(sam, axes.xMin, axes.xMax)
    #drawXIntercepts(xInts,  canvas, axes, winWidth, winHeight, "green")
    
    '''
    char = u"\u222B"
    
    anirban = Sum(parseFunction(char + "(sin(x))dx", 'x'))
    anirban.setColor("green")
    
    anirban.draw(canvas, axes, winWidth, winHeight)
    
    print(anirban.generatePoint(2))
    '''
    #s = Sum (parseFunction("x^2 +1  -2x   ", 'x'))
    #print(s.terms)
    #s.setColor("Red")
    
    #q = Sum(Id())
    #q.setColor("green")
    '''
    s = Sum(Power(2), Id())
    x = Sum(integralTaylorApproximation(s, 20, 0))
    x.setColor("green")
    r = Sum(Product(Decimal(1/3), Power(3)), Product(Decimal(1/2), Power(2)))
    r.setColor("red")
    d = Sum(Sec())
    '''
    #x = Sum(callWithLargeStack(integralTaylorApproximation, Sin(), 30, 0))
    '''
    char = u"\u222B"
    
    s = char + "(sin(x))dx "
    '''
    #cos = Sum(parseFunction("-cos(x)", 'x'))
    
    #cos.draw(canvas, axes, winWidth, winHeight)
    '''
    print(cos)
    
    c = Sum(parseFunction("-cos(x)", 'x'))
    c.setColor('red')
    c.draw(canvas, axes, winWidth, winHeight)
    print(canvas.location(400,400))
    '''
    
    #x = Sum(Power(0.5))
    #y = Sum(Cos())
    #p = Parametric(x,y, 0, 3.14159265)
    #x.draw(canvas, axes, winWidth, winHeight)
   # x =x.deriv()
    #x.setColor("red")
    #x.draw(canvas, axes, winWidth, winHeight)

    
    #Polar(q, 0, 60).draw(canvas, axes, winWidth, winHeight)
    #d.draw(canvas, axes, winWidth, winHeight)
    #x.draw(canvas, axes, winWidth, winHeight)
    #r.draw(canvas, axes, winWidth, winHeight)
    
    root.mainloop()
    
    
if __name__ == '__main__':
    main()
    
    
    

        
        