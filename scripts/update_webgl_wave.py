#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhances the WebGL blue-and-purple silk wave background (`4143-6b83e17252ec01c2.js`)
so that the wave continuously undulates, flows, and ripples in 3D and UV space even
when the mouse is idle, while preserving smooth cursor interaction.
"""

import os

ROOT = "/home/antigravity/Roasist/roasist-web"

OLD_POST_FRAG = (
    'float uRandom = ").concat(Math.random(),";\\n'
    '\tvarying vec3 vPosition;\\n\\n'
    '\tuniform sampler2D tDiffuse;\\n\\n'
    '\tvarying vec2 vUv;\\n\\n'
    '\t").concat(l,"\\n'
    '\t\\n'
    '\tfloat pattern() {\\n\\n'
    '\t\tfloat s = sin( angle ), c = cos( angle );\\n\\n'
    '\t\tvec2 tex = vUv * tSize - center;\\n'
    '\t\tvec2 point = vec2( c * tex.x - s * tex.y, s * tex.x + c * tex.y ) * scale;\\n\\n'
    '\t\treturn ( sin( point.x ) * sin( point.y ) ) * 4.0;\\n\\n'
    '\t}\\n\\n'
    'void main() {\\n'
    '  vec2 newUv = vUv;\\n'
    '  float aspect = max(tSize.x / max(tSize.y, 1.0), 1.0);\\n'
    '  vec2 mouseUv = vec2(uMouse.x + 0.5, 0.5 - uMouse.y);\\n'
    '  vec2 toFrag = (vUv - mouseUv) * vec2(aspect, 1.0);\\n'
    '  float mDist = length(toFrag);\\n'
    '  float hm = uHover * uMouseEffect;\\n'
    '  float wideProx = exp(-mDist * mDist * 2.0) * hm;\\n'
    '  float midProx = exp(-mDist * mDist * 4.8) * hm;\\n'
    '  float tightProx = exp(-mDist * mDist * 8.5) * hm;\\n'
    '  vec2 flowVec = vec2(uFlow.x, -uFlow.y);\\n'
    '  float flowMag = clamp(length(flowVec) * 2.8, 0.0, 1.5);\\n'
    '  vec2 radialDir = toFrag / (mDist + 0.30);\\n'
    '  vec2 perpDir = vec2(-toFrag.y, toFrag.x) / (mDist + 0.30);\\n'
    '  float rippleWave = sin(mDist * 9.0 - uTime * 2.8 - uFlowAccum * 3.0) * midProx * (0.34 + 0.75 * flowMag);\\n'
    '  vec2 silkBend = radialDir * (midProx * 0.46 + rippleWave * 0.28) + perpDir * (tightProx * (0.28 + 0.85 * flowMag)) - flowVec * wideProx * 2.8;\\n'
    '  vec2 mPhase = uMouse * hm * 2.4;\\n'
    '  vec2 p = 2. * vUv - vec2(1.) + silkBend;\\n'
    '  p += 0.3 * uRandom * cos(2. * (p.yx * uRandom) + uTime + mPhase.x * 1.2);\\n'
    '  p += 0.4 * uRandom * cos(5. * (p.xy * uRandom) + 1.5 * uTime - mPhase.y * 1.5);\\n'
    '  p += 0.2 * uRandom * cos(3.7 * p.yx + 2.5 * uTime + (mPhase.x - mPhase.y) * 1.3 + uFlowAccum * 0.5 * wideProx);\\n'
    '  p += 0.2 * cos(7. * p.yx + 0.5 * uTime + midProx * (1.2 + 1.4 * flowMag) + rippleWave * 1.35);\\n'
    '  vec2 centredUv = 2. * vUv - vec2(1.);\\n'
    '  newUv = vUv + centredUv * vec2(1., 1.);\\n'
    '  float dynAmount = uAmount + midProx * (0.062 + 0.075 * flowMag);\\n'
    '  vec2 directPull = flowVec * wideProx * 0.15 + radialDir * tightProx * 0.048 + perpDir * rippleWave * 0.04;\\n'
    '  newUv.x = mix(vUv.x, length(p), dynAmount) - directPull.x;\\n'
    '  newUv.y = mix(vUv.y, 0., dynAmount) - directPull.y;\\n'
    '  vec4 color = texture2D( tDiffuse, newUv );\\n'
    '  gl_FragColor = vec4(color.xyz, 1.);\\n'
    '}")}'
)

NEW_POST_FRAG = (
    'float uRandom = 0.88;\\n'
    '\tvarying vec3 vPosition;\\n\\n'
    '\tuniform sampler2D tDiffuse;\\n\\n'
    '\tvarying vec2 vUv;\\n\\n'
    '\t").concat(l,"\\n'
    '\t\\n'
    '\tfloat pattern() {\\n\\n'
    '\t\tfloat s = sin( angle ), c = cos( angle );\\n\\n'
    '\t\tvec2 tex = vUv * tSize - center;\\n'
    '\t\tvec2 point = vec2( c * tex.x - s * tex.y, s * tex.x + c * tex.y ) * scale;\\n\\n'
    '\t\treturn ( sin( point.x ) * sin( point.y ) ) * 4.0;\\n\\n'
    '\t}\\n\\n'
    'void main() {\\n'
    '  vec2 newUv = vUv;\\n'
    '  float aspect = max(tSize.x / max(tSize.y, 1.0), 1.0);\\n'
    '  vec2 mouseUv = vec2(uMouse.x + 0.5, 0.5 - uMouse.y);\\n'
    '  vec2 toFrag = (vUv - mouseUv) * vec2(aspect, 1.0);\\n'
    '  float mDist = length(toFrag);\\n'
    '  float hm = uHover * uMouseEffect;\\n'
    '  float wideProx = exp(-mDist * mDist * 2.0) * hm;\\n'
    '  float midProx = exp(-mDist * mDist * 4.8) * hm;\\n'
    '  float tightProx = exp(-mDist * mDist * 8.5) * hm;\\n'
    '  vec2 flowVec = vec2(uFlow.x, -uFlow.y);\\n'
    '  float flowMag = clamp(length(flowVec) * 2.8, 0.0, 1.5);\\n'
    '  vec2 radialDir = toFrag / (mDist + 0.30);\\n'
    '  vec2 perpDir = vec2(-toFrag.y, toFrag.x) / (mDist + 0.30);\\n'
    '  float rippleWave = sin(mDist * 9.0 - uTime * 2.8 - uFlowAccum * 3.0) * midProx * (0.34 + 0.75 * flowMag);\\n'
    '  vec2 silkBend = radialDir * (midProx * 0.46 + rippleWave * 0.28) + perpDir * (tightProx * (0.28 + 0.85 * flowMag)) - flowVec * wideProx * 2.8;\\n'
    '  vec2 mPhase = uMouse * hm * 2.4;\\n'
    '  vec2 waveOffset = vec2(\\n'
    '    sin(vUv.y * 5.2 - uTime * 1.45) * 0.042 + cos((vUv.x + vUv.y) * 4.0 + uTime * 1.15) * 0.028,\\n'
    '    cos(vUv.x * 4.6 - uTime * 1.30) * 0.045 + sin((vUv.y - vUv.x) * 3.7 + uTime * 1.55) * 0.030\\n'
    '  );\\n'
    '  vec2 p = 2. * (vUv + waveOffset * 0.65) - vec2(1.) + silkBend;\\n'
    '  p += 0.36 * uRandom * cos(2.2 * (p.yx * uRandom) + uTime * 1.15 + mPhase.x * 1.2);\\n'
    '  p += 0.46 * uRandom * cos(4.8 * (p.xy * uRandom) + 1.65 * uTime - mPhase.y * 1.5);\\n'
    '  p += 0.26 * uRandom * cos(3.7 * p.yx + 2.4 * uTime + (mPhase.x - mPhase.y) * 1.3 + uFlowAccum * 0.5 * wideProx);\\n'
    '  p += 0.25 * cos(6.8 * p.yx + 0.85 * uTime + midProx * (1.2 + 1.4 * flowMag) + rippleWave * 1.35);\\n'
    '  vec2 centredUv = 2. * vUv - vec2(1.);\\n'
    '  newUv = vUv + centredUv * vec2(1., 1.);\\n'
    '  float dynAmount = uAmount + 0.038 + 0.024 * sin(uTime * 0.95 + vUv.y * 3.14159) + midProx * (0.062 + 0.075 * flowMag);\\n'
    '  vec2 directPull = flowVec * wideProx * 0.15 + radialDir * tightProx * 0.048 + perpDir * rippleWave * 0.04;\\n'
    '  newUv.x = mix(vUv.x, length(p), dynAmount) + waveOffset.x - directPull.x;\\n'
    '  newUv.y = mix(vUv.y, sin(p.y * 1.5 + uTime * 0.85) * 0.18, dynAmount) + waveOffset.y - directPull.y;\\n'
    '  newUv = clamp(newUv, 0.002, 0.998);\\n'
    '  vec4 color = texture2D( tDiffuse, newUv );\\n'
    '  gl_FragColor = vec4(color.xyz, 1.);\\n'
    '}")}'
)

OLD_PLANE_SHADERS = (
    'v="\\nvarying vec2 uPos;\\nvarying vec2 vUv;\\nuniform vec2 uRayMouse;\\nuniform float uMouseEffect;\\n\\n'
    'uniform float uRatio;\\nfloat uTrailWidth = 0.15; \\nfloat PI = ".concat(Math.PI,";\\n\\n'
    'void main() {\\n'
    '    vUv = uv;\\n    \\n'
    '    vec2 direction = normalize(position.xy - uRayMouse);\\n    \\n'
    '    float distanceToMouse = length(position.xy - uRayMouse);\\n    \\n'
    '    float falloff = smoothstep(0., uTrailWidth, distanceToMouse);\\n    \\n'
    '    float displacement = uMouseEffect * 0.1 * falloff;\\n'
    '    // float displacementY = uMouseEffect * 0.1 * falloff * uRatio;\\n\\n'
    '    // float displacement = mix(displacementX, displacementY, 1.5);\\n    \\n'
    '    vec3 newPosition = vec3(position.xy - direction * displacement / 2., position.z );\\n    \\n'
    '    uPos = direction * displacement * 2.;\\n    \\n'
    '    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);\\n'
    '}\\n  "),f="\\n  uniform float uTime;\\n  uniform vec2 uRayMouse;\\n  uniform float uMouseEffect;\\n'
    '  uniform float uNoiseAmount;\\n  uniform float uAmount;\\n  uniform float uPow;\\n  uniform float uAlpha;\\n'
    '  varying vec2 vUv;\\n  varying vec2 uPos;\\n  uniform vec3 uColor[".concat(d.length,"];\\n'
    '  float PI = ").concat(Math.PI,";\\n\\n  ").concat(l,"\\n    \\n'
    '  void main() {\\n'
    '    vec3 firstColor = uColor[0];\\n'
    '    vec2 seed = (vUv * -uPos) * mix(vUv, uPos, 30. * uAmount);\\n'
)

NEW_PLANE_SHADERS = (
    'v="\\nvarying vec2 uPos;\\nvarying vec2 vUv;\\nuniform vec2 uRayMouse;\\nuniform float uMouseEffect;\\n'
    'uniform float uVelocity;\\nuniform float uRatio;\\nfloat uTrailWidth = 0.19; \\nfloat PI = ".concat(Math.PI,";\\n\\n'
    'void main() {\\n'
    '    vUv = uv;\\n'
    '    float wt = uVelocity * 1.15;\\n'
    '    vec2 direction = normalize(position.xy - uRayMouse);\\n'
    '    float distanceToMouse = length(position.xy - uRayMouse);\\n'
    '    float falloff = smoothstep(0., uTrailWidth, distanceToMouse);\\n'
    '    float displacement = uMouseEffect * 0.12 * falloff;\\n'
    '    uPos = direction * displacement * 2.2;\\n'
    '    vec3 pos = position;\\n'
    '    pos.x += sin(uv.y * 4.8 - wt * 1.35) * 0.08 + cos(uv.x * 3.6 + wt * 0.95) * 0.04;\\n'
    '    pos.y += cos(uv.x * 4.4 - wt * 1.20) * 0.08 + sin(uv.y * 3.8 + wt * 1.10) * 0.04;\\n'
    '    pos.z += sin((uv.x * 3.5 + uv.y * 4.2) - wt * 1.45) * 0.12;\\n'
    '    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);\\n'
    '}\\n  "),f="\\n  uniform float uTime;\\n  uniform float uVelocity;\\n  uniform vec2 uRayMouse;\\n  uniform float uMouseEffect;\\n'
    '  uniform float uNoiseAmount;\\n  uniform float uAmount;\\n  uniform float uPow;\\n  uniform float uAlpha;\\n'
    '  varying vec2 vUv;\\n  varying vec2 uPos;\\n  uniform vec3 uColor[".concat(d.length,"];\\n'
    '  float PI = ").concat(Math.PI,";\\n\\n  ").concat(l,"\\n    \\n'
    '  void main() {\\n'
    '    vec3 firstColor = uColor[0];\\n'
    '    float wt = uVelocity * 0.95;\\n'
    '    vec2 waveUv = vUv + vec2(\\n'
    '      sin(vUv.y * 4.5 - wt * 1.25) * 0.065 + cos(vUv.x * 3.4 + wt * 0.9) * 0.038,\\n'
    '      cos(vUv.x * 4.2 - wt * 1.15) * 0.065 + sin(vUv.y * 3.6 + wt * 1.05) * 0.038\\n'
    '    );\\n'
    '    vec2 seed = (waveUv * -uPos) * mix(waveUv, uPos, 30. * uAmount);\\n'
)

OLD_RENDER = (
    'render(){if(!1===this.isPlaying)return;'
    'this.time+=.01,'
    'this.reverseUTime?(this.uTime-=.001,this.uTime<.1&&(this.reverseUTime=!1)):(this.uTime+=.001,this.uTime>.5&&(this.reverseUTime=!0));'
    'let hv=this.uHover.value,dx=(this.uMouseFast.x-this.uMouse.x)*3.2,dy=(this.uMouseFast.y-this.uMouse.y)*3.2;'
    'this.uFlow.set(this.uFlow.x*.82+dx*.18,this.uFlow.y*.82+dy*.18);'
    'this.flowAccum+=Math.min(.16,Math.hypot(this.uFlow.x,this.uFlow.y)*.28)*hv;'
    'this.plane&&(this.plane.rotation.x=-this.uMouse.y*.2*hv,this.plane.rotation.y=this.uMouse.x*.26*hv);'
    'this.camera&&(this.camera.position.x=(this.activeBackground.position.x-this.uMouse.x*.058*hv)*this.width,this.camera.position.y=-(this.activeBackground.position.y-this.uMouse.y*.058*hv)*this.height);'
    'this.material.uniforms.uTime.value=this.uTime,'
    'this.material.uniforms.uRayMouse.value=this.rayMouse,'
)

NEW_RENDER = (
    'render(){if(!1===this.isPlaying)return;'
    'this.time+=.026,'
    'this.reverseUTime?(this.uTime-=.0034,this.uTime<.12&&(this.reverseUTime=!1)):(this.uTime+=.0034,this.uTime>.48&&(this.reverseUTime=!0));'
    'let hv=this.uHover.value,dx=(this.uMouseFast.x-this.uMouse.x)*3.2,dy=(this.uMouseFast.y-this.uMouse.y)*3.2;'
    'this.uFlow.set(this.uFlow.x*.82+dx*.18,this.uFlow.y*.82+dy*.18);'
    'this.flowAccum+=Math.min(.16,Math.hypot(this.uFlow.x,this.uFlow.y)*.28)*hv;'
    'let wt=this.time*.92;'
    'if(this.allowRayMouse){'
    'let tx=-.4+Math.sin(wt*1.15)*.26+Math.cos(wt*.67)*.15+this.uMouse.x*.46*hv,'
    'ty=-.4+Math.cos(wt*.92)*.24+Math.sin(wt*1.42)*.14-this.uMouse.y*.46*hv;'
    'this.rayMouse.x+=(tx-this.rayMouse.x)*.08,this.rayMouse.y+=(ty-this.rayMouse.y)*.08'
    '}'
    'let rx=Math.sin(wt*.95)*.17+Math.cos(wt*.53)*.08,ry=Math.cos(wt*.82)*.21+Math.sin(wt*1.25)*.09,rz=Math.sin(wt*.64)*.11;'
    'this.plane&&(this.plane.rotation.x=rx-this.uMouse.y*.22*hv,this.plane.rotation.y=ry+this.uMouse.x*.28*hv,this.plane.rotation.z=Math.sin(wt*.56)*.08);'
    'this.camera&&(this.camera.position.x=(this.activeBackground.position.x+Math.sin(wt*.74)*.044-this.uMouse.x*.058*hv)*this.width,this.camera.position.y=-(this.activeBackground.position.y+Math.cos(wt*.86)*.042-this.uMouse.y*.058*hv)*this.height,this.camera.rotation.z=this.activeBackground.rotation+rz);'
    'this.material.uniforms.uTime.value=this.uTime,'
    'this.material.uniforms.uVelocity.value=this.time,'
    'this.material.uniforms.uRayMouse.value=this.rayMouse,'
)


def update_chunk(fp: str) -> bool:
    txt = open(fp, "r", encoding="utf-8").read()
    updated = txt

    if OLD_POST_FRAG in updated:
        updated = updated.replace(OLD_POST_FRAG, NEW_POST_FRAG, 1)
    elif NEW_POST_FRAG not in updated:
        raise RuntimeError(f"Could not find OLD_POST_FRAG in {fp}")

    if OLD_PLANE_SHADERS in updated:
        updated = updated.replace(OLD_PLANE_SHADERS, NEW_PLANE_SHADERS, 1)
    elif NEW_PLANE_SHADERS not in updated:
        raise RuntimeError(f"Could not find OLD_PLANE_SHADERS in {fp}")

    if OLD_RENDER in updated:
        updated = updated.replace(OLD_RENDER, NEW_RENDER, 1)
    elif NEW_RENDER not in updated:
        raise RuntimeError(f"Could not find OLD_RENDER in {fp}")

    if updated != txt:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(updated)
        return True
    return False


def sync_dist_chunk_sha(new_sha: str) -> int:
    import glob
    import re

    pat = re.compile(
        r"https://cdn\.jsdelivr\.net/gh/Roasist/roasist-web@[0-9a-f]{40}/public/_next/static/chunks/4143-6b83e17252ec01c2\.js"
    )
    target = f"https://cdn.jsdelivr.net/gh/Roasist/roasist-web@{new_sha}/public/_next/static/chunks/4143-6b83e17252ec01c2.js"
    updated_files = 0
    for fp in sorted(glob.glob(os.path.join(ROOT, "dist", "**", "*.html"), recursive=True)):
        txt = open(fp, "r", encoding="utf-8").read()
        new_txt, n = pat.subn(target, txt)
        if n > 0 and new_txt != txt:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(new_txt)
            updated_files += 1
    print(f"[WEBGL WAVE] Synced dist HTML chunk SHA to {new_sha} across {updated_files} files")
    return updated_files


def main():
    import sys

    count = 0
    for base in ("public", "dist"):
        fp = os.path.join(ROOT, base, "_next", "static", "chunks", "4143-6b83e17252ec01c2.js")
        if update_chunk(fp):
            count += 1
    print(f"[WEBGL WAVE] Updated {count} chunk files (public + dist)")

    if len(sys.argv) >= 3 and sys.argv[1] == "--sync-dist-sha":
        sync_dist_chunk_sha(sys.argv[2].strip())


if __name__ == "__main__":
    main()
