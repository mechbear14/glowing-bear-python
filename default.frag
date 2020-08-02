#version 430 core

in vec2 bottomLeft;
in vec2 size;
out vec4 colour;

void main(){
    vec2 u_resolution = vec2(1280.0, 720.0);
    vec2 st = gl_FragCoord.xy / u_resolution.xy * 2.0 - vec2(1.0, 1.0);
    st = (st - bottomLeft) / size.xy;
    float maskX = smoothstep(0.0, 0.1, st.x) - smoothstep(0.9, 1.0, st.x);
    float maskY = smoothstep(0.0, 0.1, st.y) - smoothstep(0.9, 1.0, st.y);
    float mask = maskX * maskY;
    colour = vec4(0.0, 0.8, 1.0, 1.0) * mask;
}
