import gtk, pango
import math


class Sheet:
    def __init__(self, context, paper_size='a4'):
        if context.__class__ == gtk.DrawingArea:
            self.pango_layout = context.create_pango_layout("")
            self.cairo_context = context.window.cairo_create()
            self.type = 'area'
            self.width, self.height = context.size_request()
            self.factor = 1
        elif context.__class__ == gtk.PrintContext:
            self.pango_layout = context.create_pango_layout()
            self.cairo_context = context.get_cairo_context()
            self.type = 'print'
            self.width = context.get_width()
            self.height = context.get_height()
            self.factor = 5.9 # .25
        
        self.paper_size = paper_size.lower()
        if self.paper_size == 'a4':
            self.aspect_ratio = math.sqrt(2)
                    
            
    def set_pen(self, x_pos=None, y_pos=None, line_width=None, color='#000000'):
        if x_pos <> None and y_pos <> None:
            self.cairo_context.move_to(x_pos*self.factor, y_pos*self.factor)
        if line_width <> None:
            self.cairo_context.set_line_width(line_width*self.factor)
        return


    def draw(self):
        pass
        
        
        
class Text:
    def __init__(self, sheet_object):
        self.sheet = sheet_object
        self.cairo_context = sheet_object.cairo_context
        self.pango_layout = sheet_object.pango_layout
        self.factor = sheet_object.factor
        
        
    def set_font(self, font='courier new 12'):
        font_description = pango.FontDescription(font)
        self.pango_layout.set_font_description(font_description)
        
        
    def draw(self, text='', x_pos=0, y_pos=0, width=0, height=0, justify=False):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        
        self.sheet.set_pen(self.x_pos, self.y_pos)
        self.pango_layout.set_width(int(self.width*self.factor))
        # self.pango_layout.set_wrap(pango.WRAP_CHAR)
        
        if justify == True:
            self.pango_layout.set_justify(justify=True)
        
        print 'pixel_size:', self.pango_layout.get_pixel_size(), 'width:', self.pango_layout.get_width()
        
        self.pango_layout.set_text(unicode(self.text, 'latin-1'))
        self.cairo_context.show_layout(self.pango_layout)
        
        
        
class Line:
    def __init__(self, sheet_object):
        self.sheet = sheet_object
        self.cairo_context = self.sheet.cairo_context
        self.factor = sheet_object.factor
        
        
    def draw(self, point_lol=[], line_width=1):
        ''' point_lol = [[x, y], [x, y], ...]
                List of lists which contains coordinates of points. '''
        
        self.point_lol = point_lol
        self.line_width = line_width
        x_pos, y_pos = self.point_lol[0]
        self.sheet.set_pen(x_pos, y_pos, self.line_width)
        
        for x_pos, y_pos in self.point_lol:
            self.cairo_context.line_to(x_pos*self.factor, y_pos*self.factor)
        
        self.cairo_context.stroke()
        
        
        
class Circle:
    def __init__(self, sheet_object):
        self.sheet = sheet_object
        self.cairo_context = sheet_object.cairo_context
        self.factor = sheet_object.factor
        
    
    def draw(self, x_pos=0, y_pos=0, radius=0, line_width=1):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.line_width = line_width
        
        self.sheet.set_pen(None, None, self.line_width)
        self.cairo_context.arc(self.x_pos*self.factor, self.y_pos*self.factor, self.radius*self.factor, 0, 360 * (math.pi / 180))
        self.cairo_context.stroke()

        
        
class Ellipse:
    def __init__(self, sheet_object):
        self.sheet = sheet_object
        self.cairo_context = sheet_object.cairo_context
        self.factor = sheet_object.factor
        

        
class Image:
    def __init__(self, sheet_object):
        self.sheet = sheet_object
        self.cairo_context = sheet_object.cairo_context
        self.factor = sheet_object.factor
        
    
    def draw(self, filename='', x_pos=0, y_pos=0, width=0, height=0):
        self.filename = filename
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        
        

