#version 430 core

in vec2 position;
out vec2 bottomLeft;
out vec2 size;

void main(){
    gl_Position = vec4(position, 0.0, 1.0);
    bottomLeft = vec2(-0.3 + abs(position.x) / position.x * 0.4, -0.3);
    size = vec2(0.6, 0.6);
}