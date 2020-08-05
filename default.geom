#version 430 core

layout(points) in;
layout(triangle_strip, max_vertices=6) out;
out vec2 bottomLeft;
uniform vec2 size;

void main(){
    bottomLeft = gl_in[0].gl_Position.xy - size.xy / 2.0;
    vec2 bottomRight = gl_in[0].gl_Position.xy - vec2(size.x / 2.0, -size.y / 2.0);
    vec2 topLeft = gl_in[0].gl_Position.xy - vec2(-size.x / 2.0, size.y / 2.0);
    vec2 topRight = gl_in[0].gl_Position.xy - vec2(-size.x / 2.0, -size.y / 2.0);

    gl_Position = vec4(bottomLeft, 0.0, 1.0);
    EmitVertex();
    gl_Position = vec4(bottomRight, 0.0, 1.0);
    EmitVertex();
    gl_Position = vec4(topLeft, 0.0, 1.0);
    EmitVertex();
    gl_Position = vec4(topRight, 0.0, 1.0);
    EmitVertex();
    EndPrimitive();
}