#this file represents the statistics framework for the project. It has a 
#scatterplot object which can plot points and calculate regression

from Terms import *
#from Utility import *

class ScatterPlot(object):
    
    def __init__(self, *args):
        
        self.data = []
        if type(args[0] ) == list:
            for coordinate in args[0]:
                self.data.append(coordinate)
        else:
            for coordinate in args:
                self.data.append(coordinate)
        self.color = "red"
        
    def setColor(color):
        self.color = color
        
    #autoset the axes for the user
    def draw(self, canvas, axes, winWidth, winHeight):
        
        graphicsPoints = convertPoints(self.data, axes, winWidth, winHeight)
        for i in range(len( graphicsPoints )):
            
            point = graphicsPoints[i]
            cx = point[0]
            cy = point[1]
            r = 5
            canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = self.color, \
            width = 0)
            
            xVal = self.data[i][0]
            yVal = self.data[i][1]
            
            labelPoint(canvas, cx, cy, xVal, yVal, 5)
            
        
            
    def autoSetAxes(self, axes):
        
        xMin = self.data[0][0]
        xMax = self.data[0][0]
        yMin = self.data[0][1]
        yMax = self.data[0][1]
        
        for point in self.data:
            x = point[0]
            y = point[1]
            
            if x > xMax:
                xMax = x
            if x < xMin:
                xMin = x
            if y > yMax:
                yMax = y
            if y < yMin:
                yMin = y
        
        
        domain = xMax - xMin
        range = yMax - yMin
        
        
        expansion = 0.1
        
        axes.xMin = xMin - expansion*domain
        axes.xMax = xMax + expansion*domain
        axes.yMin = yMin - expansion*range
        axes.yMax = yMax + expansion*range
        axes.setVisualScales()
            
    def calculateRegression(self):
        
        
        xBar = 0
        yBar = 0
        
        sumX = 0
        sumY = 0
        for p in self.data:
            sumX += p[0]
            sumY += p[1]
            
        xBar = sumX/len(self.data)
        yBar = sumY/len(self.data)
        
        num = 0
        denom = 0
        
        for p in self.data:
            num += (p[0] - xBar)*(p[1]-yBar)
            denom += (p[0] - xBar)**2
        slope = num/denom
        
        intercept = yBar - slope*xBar
        
        return Sum(Product(Decimal(slope), Id()), Decimal(intercept))
    
    def drawRegression(self, canvas, axes, winWidth, winHeight):
            
        regression = self.calculateRegression()
        regression.draw( canvas, axes, winWidth, winHeight)
        self.draw(canvas, axes, winWidth, winHeight)
        r = self.calculateR()
        
        if r > 0:
            canvas.create_text(20,5, text = "r = %0.3f" % r, font = \
            "Times 16", anchor = NW)
            canvas.create_text(20,25, text = "r^2 = %0.3f" % r**2, font = \
            "Times 16", anchor = NW)
            canvas.create_text(20,45, text = "y = %s" % \
            str(self.calculateRegression()), font = "Times 16", anchor = NW)
        else:
            canvas.create_text(20,winHeight - 45, text = "r = %0.3f" % r, \
            font = "Times 16", anchor = SW)
            canvas.create_text(20,winHeight - 25, text = "r^2 = %0.3f" % \
            r**2, font = "Times 16", anchor = SW)
            canvas.create_text(20,winHeight - 5, text = "y = %s" % \
            str(self.calculateRegression()), font = "Times 16", anchor = SW)
    
            
    def calculateR (self):
        sumXY = 0
        sumX = 0
        sumY = 0
        sumXSquared = 0
        sumYSquared = 0
        for point in self.data:
            x = point[0]
            y = point[1]
            sumXY += x*y
            sumX += x
            sumY += y
            sumXSquared += x**2
            sumYSquared += y**2
            
        #print(sumXY, sumX, sumY, sumXSquared, sumYSquared)
        n = len(self.data)
        num = n*sumXY - sumX*sumY
        denom = ((n*sumXSquared - (sumX)**2)*(n*sumYSquared - (sumY)**2))**0.5
        
        #print(num/denom)
        return num/denom
        
    def calculateRSquared(self):
        r = self.calculateR()
        #print(r**2)
        return r**2
        
    def drawRegressionInfo(self, canvas, winHeight):
        r = self.calculateR()
        margin = 30
        rectangleMargin = 10
        rectangleLength = max(100, len("y = %s" % \
        str(self.calculateRegression()))*7)
        
        if r > 0:
            canvas.create_rectangle(margin-rectangleMargin, 5, \
            rectangleLength + margin ,65 + rectangleMargin, fill = "white")
            canvas.create_text(margin,10, text = "r = %0.3f" % r, \
            font = "Times 16", anchor = NW)
            canvas.create_text(margin,30, text = "r^2 = %0.3f" % r**2, \
            font = "Times 16", anchor = NW)
            canvas.create_text(margin,50, text = "y = %s" % \
            str(self.calculateRegression()), font = "Times 16", anchor = NW)
        else:
            canvas.create_rectangle(margin-rectangleMargin, winHeight - \
            50-margin, rectangleLength + margin, winHeight-10+rectangleMargin, \
            fill = "white")
            canvas.create_text(margin,winHeight - 50, text = "r = %0.3f" % r, \
            font = "Times 16", anchor = SW)
            canvas.create_text(margin,winHeight - 30, text = "r^2 = %0.3f" % \
            r**2, font = "Times 16", anchor = SW)
            canvas.create_text(margin,winHeight - 10, text = "y = %s" % \
            str(self.calculateRegression()), font = "Times 16", anchor = SW)
        
            
def main():
    
    winWidth = 1000
    winHeight = 800
    root = Tk()
    canvas = Canvas(root, width=winWidth, height=winHeight)
    canvas.pack()
    
    axes = Axes(-10, 10, -10, 10, 1, 1)
    
    l = [(1,0), (2,1), (3,3) ,(4,4) ,(5,5), (3,5), (5,3), (7,8), (9,12),\
     (13,9),(12,13)]
    #l = [(1,-1),(2,-3),(3,-2),(4,-4),(5,-5),(6,-5),(7,-6),(6,-6),(5,-6),\
    #(4,-6),(3,-7),(2,-2),(1,-2)]
    s = ScatterPlot(l)
    s.autoSetAxes(axes)
    
    axes.draw(canvas, winWidth, winHeight)
    s.drawRegression(canvas, axes, winWidth, winHeight)
    s.calculateRSquared()
   
    
    root.mainloop()
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    main()
 