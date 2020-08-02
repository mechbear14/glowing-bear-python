import pygame
from pygame.locals import *
from OpenGL.GL import *
import numpy

# Globals
screen_size = (1280, 720)
drawing_size = (720, 360)

pygame.init()
screen = pygame.display.set_mode(screen_size, DOUBLEBUF | OPENGL)
clock = pygame.time.Clock()

# OpenGL setup
vertices = numpy.array([-0.1, -0.3, -0.1, 0.3, -0.7, -0.3,
                        -0.7, -0.3, -0.1, 0.3, -0.7, 0.3,
                        0.7, -0.3, 0.7, 0.3, 0.1, -0.3,
                        0.1, -0.3, 0.7, 0.3, 0.1, 0.3]).astype(GLfloat)
vbo = glGenBuffers(1)
vao = glGenVertexArrays(1)
glBindVertexArray(vao)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, vertices.size * sizeof(GLfloat), vertices, GL_STATIC_DRAW)
glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * 2, None)
glEnableVertexAttribArray(0)

with open("default.vert") as vert_file:
    global vert_code
    vert_code = vert_file.read()
vert_shader = glCreateShader(GL_VERTEX_SHADER)
glShaderSource(vert_shader, vert_code)
glCompileShader(vert_shader)

with open("default.frag") as frag_file:
    global frag_code
    frag_code = frag_file.read()
frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
glShaderSource(frag_shader, frag_code)
glCompileShader(frag_shader)

program = glCreateProgram()
glAttachShader(program, vert_shader)
glAttachShader(program, frag_shader)
glLinkProgram(program)

glDeleteShader(vert_shader)
glDeleteShader(frag_shader)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            raise SystemExit
    glBindVertexArray(vao)
    glUseProgram(program)
    glDrawArrays(GL_TRIANGLES, 0, 12)
    pygame.display.flip()
    clock.tick(30)
