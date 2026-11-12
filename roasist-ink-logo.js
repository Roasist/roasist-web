(function () {
  if (typeof window === "undefined" || window.__ROASIST_INK_LOGO_V1__) return;
  window.__ROASIST_INK_LOGO_V1__ = 1;

  var BASE_W = 168;
  var BASE_H = 41;
  var PAD = { left: 32, right: 36, top: 24, bottom: 132 };
  var CV_W = BASE_W + PAD.left + PAD.right;
  var CV_H = BASE_H + PAD.top + PAD.bottom;

  var SVG_MARKUP =
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 200"><path fill="#ffffff" d="M176.71,198.48v1.32l-35.19.2c-1.72-2.67-2.88-6.5-3.64-11.52-.59-4.79-1.15-10-1.55-15.35s-.56-10.76-1-15.75a95,95,0,0,0-1.16-12.48c-1-4.42-2.51-8.08-4.62-10.56a20.66,20.66,0,0,0-7.46-6.17,32.19,32.19,0,0,0-9.81-2.88c-3.66-.36-7.29-.56-11.15-.56h-47v-35h56.29v18.62L164.6,77.1,110.46,45.8V64.42H54.17v16L0,49.07,54.17,17.74V34.08h64.9c18.26,0,32.29,3.47,41.89,10.17,9.78,6.93,14.6,18.06,14.6,33.41,0,10.4-2.12,18.85-6.34,24.79C165,108.79,158.06,114,148.65,118.2a28.6,28.6,0,0,1,11.52,7.29,35.16,35.16,0,0,1,6.18,11.13A60.62,60.62,0,0,1,169,149.69c.4,4.62.56,9.21.76,13.44.2,6.33.4,11.52.79,15.74.36,4.06,1,7.5,1.32,10A24.35,24.35,0,0,0,174,195,8.76,8.76,0,0,0,176.71,198.48Z M186,84q1.68-15.32,7.38-26.28a41.37,41.37,0,0,1,16.45-17.12q10.74-6.15,28.86-6.15t28.86,6.15A41.37,41.37,0,0,1,284,57.73q5.7,11,7.38,26.28a308.26,308.26,0,0,1,1.68,33.45A307.5,307.5,0,0,1,291.39,151q-1.68,15.21-7.38,26.17A39.24,39.24,0,0,1,267.56,194q-10.74,5.82-28.86,5.82T209.84,194a39.24,39.24,0,0,1-16.45-16.78Q187.69,166.25,186,151a307.5,307.5,0,0,1-1.68-33.57A308.26,308.26,0,0,1,186,84Zm31.32,60.86a76.29,76.29,0,0,0,3.13,18.35q2.35,7,6.72,10.29c2.91,2.17,6.74,3.25,11.52,3.25s8.61-1.08,11.52-3.25,5.15-5.59,6.71-10.29a76.24,76.24,0,0,0,3.14-18.35q.78-11.3.78-27.41t-.78-27.29a77.72,77.72,0,0,0-3.14-18.35q-2.34-7.16-6.71-10.4T238.7,58.17c-4.78,0-8.61,1.09-11.52,3.25s-5.15,5.63-6.72,10.4a77.78,77.78,0,0,0-3.13,18.35q-.78,11.19-.78,27.29T217.33,144.87Z M383,37.59,425.3,197.34H391.74l-7.39-33.79H341.84l-7.38,33.79H300.9L343.19,37.59Zm-4.25,99.56L363.32,65.33h-.44l-15.44,71.82Z M462.44,152.14a53,53,0,0,0,.9,10.18,17.61,17.61,0,0,0,3.35,7.72,16.6,16.6,0,0,0,6.6,4.93,26.39,26.39,0,0,0,10.41,1.79A20.56,20.56,0,0,0,497,172q5.92-4.81,5.93-14.88a26.93,26.93,0,0,0-1.45-9.29,18.47,18.47,0,0,0-4.82-7.05,34.1,34.1,0,0,0-8.83-5.7,126.18,126.18,0,0,0-13.54-5.26,115.68,115.68,0,0,1-18.57-7.83,49.79,49.79,0,0,1-13.09-10,35.53,35.53,0,0,1-7.72-13.2,55.56,55.56,0,0,1-2.46-17.34q0-23.72,13.2-35.35t36.25-11.63a79.06,79.06,0,0,1,19.8,2.34,41.63,41.63,0,0,1,15.66,7.61,35.58,35.58,0,0,1,10.29,13.43q3.69,8.16,3.69,19.57v4.48H500.48q0-11.42-4-17.56T483,58.17a22.43,22.43,0,0,0-8.95,1.57,15.1,15.1,0,0,0-5.71,4.14,14.16,14.16,0,0,0-2.91,5.93,30.48,30.48,0,0,0-.78,6.93,23.06,23.06,0,0,0,3.13,12.42q3.13,5,13.43,9.29l24.83,10.74a75.73,75.73,0,0,1,15,8.39,41,41,0,0,1,9.29,9.39,31.46,31.46,0,0,1,4.81,11.08,62.31,62.31,0,0,1,1.34,13.42q0,25.29-14.65,36.81T481,199.8q-27.3,0-39-11.86t-11.75-34v-6.48h32.22Z M554.17,37.59h32.22V197.34H554.17ZM582.81,26.4H557.75V0h25.06Z M636.29,152.14a53.81,53.81,0,0,0,.89,10.18,17.74,17.74,0,0,0,3.36,7.72,16.6,16.6,0,0,0,6.6,4.93,26.37,26.37,0,0,0,10.4,1.79A20.59,20.59,0,0,0,670.86,172q5.92-4.81,5.93-14.88a26.68,26.68,0,0,0-1.46-9.29,18.33,18.33,0,0,0-4.81-7.05,34.17,34.17,0,0,0-8.84-5.7,125.1,125.1,0,0,0-13.53-5.26,115.68,115.68,0,0,1-18.57-7.83,49.63,49.63,0,0,1-13.09-10,35.53,35.53,0,0,1-7.72-13.2,55.56,55.56,0,0,1-2.46-17.34q0-23.72,13.2-35.35t36.24-11.63a79.2,79.2,0,0,1,19.81,2.34,41.63,41.63,0,0,1,15.66,7.61,35.58,35.58,0,0,1,10.29,13.43Q705.2,66,705.2,77.41v4.48H674.33q0-11.42-4-17.56t-13.43-6.16a22.46,22.46,0,0,0-9,1.57,15,15,0,0,0-5.7,4.14,14.16,14.16,0,0,0-2.91,5.93,29.93,29.93,0,0,0-.78,6.93,23.06,23.06,0,0,0,3.13,12.42q3.14,5,13.42,9.29l24.84,10.74a76,76,0,0,1,15,8.39A41,41,0,0,1,704.2,127a31.44,31.44,0,0,1,4.8,11.08,61.66,61.66,0,0,1,1.35,13.42q0,25.29-14.66,36.81T654.86,199.8q-27.3,0-39-11.86t-11.75-34v-6.48h32.22Z M820,64h-34.9V197.34H752.86V64H718V37.59H820Z"/></svg>';

  var VS =
    "attribute vec2 a_pos;varying vec2 v_uv;void main(){v_uv=a_pos*0.5+0.5;v_uv.y=1.0-v_uv.y;gl_Position=vec4(a_pos,0.0,1.0);}";

  var FS = [
    "#extension GL_OES_standard_derivatives : enable",
    "precision highp float;",
    "varying vec2 v_uv;",
    "uniform sampler2D u_tex;",
    "uniform float u_progress;",
    "uniform float u_dark;",
    "uniform vec3 u_baseCol;",
    "uniform vec2 u_res;",
    "uniform vec4 u_logoRect;",
    "float hash(vec2 p){p=fract(p*vec2(127.1,311.7));p+=dot(p,p+34.23);return fract(p.x*p.y);}",
    "float noise(vec2 p){vec2 i=floor(p);vec2 f=fract(p);vec2 u=f*f*(3.0-2.0*f);return mix(mix(hash(i),hash(i+vec2(1.0,0.0)),u.x),mix(hash(i+vec2(0.0,1.0)),hash(i+vec2(1.0,1.0)),u.x),u.y);}",
    "float fbm(vec2 p){float v=0.0;float a=0.5;mat2 rot=mat2(0.80,0.60,-0.60,0.80);for(int i=0;i<4;i++){v+=a*noise(p);p=rot*p*2.03+vec2(13.7,9.2);a*=0.5;}return v;}",
    "float smax(float a,float b,float k){float h=clamp(0.5+0.5*(b-a)/k,0.0,1.0);return mix(a,b,h)+k*h*(1.0-h);}",
    "float rivuletChannel(float lx){",
    "  float a=pow(0.5+0.5*sin(lx*45.0-0.8),4.0);",
    "  float b=pow(0.5+0.5*sin(lx*79.0+1.9),5.5)*0.72;",
    "  float c=pow(0.5+0.5*cos(lx*27.0+0.4),3.2)*0.55;",
    "  float env=0.58+0.42*sin(lx*19.0+2.4);",
    "  return clamp((a+b+c)*env,0.0,1.22);",
    "}",
    "void main(){",
    "  float p=clamp(u_progress,0.0,1.0);",
    "  vec2 px=v_uv*u_res;",
    "  float logoTopPx=u_logoRect.y*u_res.y;",
    "  float logoH_Px=u_logoRect.w*u_res.y;",
    "  float logoLeftPx=u_logoRect.x*u_res.x;",
    "  float logoW_Px=u_logoRect.z*u_res.x;",
    "  float lx=(px.x-logoLeftPx)/logoW_Px;",
    "  float ly=(px.y-logoTopPx)/logoH_Px;",
    "  float regionVar=(noise(vec2(lx*6.0+2.3,4.1))-0.5)*0.10;",
    "  float lp=clamp(p*1.08+regionVar*smoothstep(0.0,0.25,p)*(1.0-smoothstep(0.75,0.98,p)),0.0,1.0);",
    "  float n1=fbm(vec2(lx*5.2+1.7,px.y*0.032-lp*2.0));",
    "  float n2=fbm(vec2(lx*11.5-3.1,px.y*0.062-lp*2.9));",
    "  float yDist=max(0.0,px.y-logoTopPx);",
    "  float curlX=((n1-0.5)*7.5+(n2-0.5)*3.2)*pow(lp,1.15)*(0.25+0.85*clamp(yDist/100.0,0.0,1.0));",
    "  float bodySagPx=(4.0+14.0*pow(lp,1.4))*pow(lp,1.25);",
    "  vec2 bodyUV=vec2((px.x+curlX*0.55)/u_res.x,(px.y-bodySagPx)/u_res.y);",
    "  vec4 bodyTex=texture2D(u_tex,bodyUV);",
    "  float bodyBase=mix(bodyTex.r,mix(bodyTex.g,bodyTex.b,smoothstep(0.08,0.45,lp)),smoothstep(0.0,0.14,lp));",
    "  float blotch=fbm(vec2(lx*9.0+1.2,ly*3.2-lp*1.3));",
    "  float letterErode=smoothstep(0.14,0.68,lp*1.06+(1.0-clamp(ly,0.0,1.2))*0.25*lp+(blotch-0.5)*0.34*lp);",
    "  float letterField=clamp(bodyBase-letterErode*0.98,0.0,1.0);",
    "  float chanLx=(px.x+curlX*0.7-logoLeftPx)/logoW_Px;",
    "  float chan=rivuletChannel(chanLx);",
    "  float maxPourPx=(12.0+86.0*chan)*pow(lp,1.18);",
    "  float drainProg=clamp((lp-0.24)/0.68,0.0,1.0);",
    "  float minPourPx=maxPourPx*0.94*pow(drainProg,1.35);",
    "  float pourField=0.0;",
    "  float streakWash=0.0;",
    "  if(lp>0.01&&maxPourPx>1.0){",
    "    for(int k=0;k<24;k++){",
    "      float fk=(float(k)+0.5)/24.0;",
    "      float distUp=mix(minPourPx,maxPourPx,fk);",
    "      float sampleY=px.y-bodySagPx-distUp;",
    "      float localSway=curlX*(1.0-0.52*fk);",
    "      vec2 sUV=vec2((px.x+localSway)/u_res.x,sampleY/u_res.y);",
    "      vec4 st=texture2D(u_tex,sUV);",
    "      float neckWave=0.78+0.22*sin(fk*9.5-lp*6.0+chanLx*28.0);",
    "      float tipBulb=0.72+0.48*exp(-pow((fk-0.88)/0.15,2.0));",
    "      float tailFade=smoothstep(0.0,0.22,fk);",
    "      float streamDensity=mix(st.g,st.b,0.52);",
    "      float lateShrink=1.0-0.42*smoothstep(0.72,0.96,lp);",
    "      float shaped=streamDensity*tipBulb*neckWave*lateShrink*mix(1.0,tailFade,smoothstep(0.24,0.58,lp));",
    "      pourField=smax(pourField,shaped*0.94,0.14);",
    "      streakWash+=st.b*(1.0-0.35*fk);",
    "    }",
    "    streakWash/=24.0;",
    "  }",
    "  float dropField=0.0;",
    "  for(int i=0;i<12;i++){",
    "    float fi=float(i);",
    "    float seed=fract(sin(fi*73.19+0.87)*43758.5453);",
    "    float ax=0.05+0.90*((fi+0.2+0.6*seed)/12.0);",
    "    float anchorUVx=u_logoRect.x+ax*u_logoRect.z;",
    "    float mass=texture2D(u_tex,vec2(anchorUVx,u_logoRect.y+u_logoRect.w*0.55)).a;",
    "    if(mass>0.22){",
    "      float locChan=rivuletChannel(ax);",
    "      float delay=0.16+0.26*fract(seed*6.3);",
    "      float dp=clamp((lp-delay)/(0.98-delay),0.0,1.0);",
    "      if(dp>0.0&&dp<1.0){",
    "        float streamTipY=logoTopPx+logoH_Px*0.75+bodySagPx+(12.0+86.0*locChan)*pow(min(lp,0.85),1.18);",
    "        float dy=streamTipY+(2.0+(26.0+28.0*seed)*pow(dp,1.40));",
    "        float dx=anchorUVx*u_res.x-curlX*0.72;",
    "        float rad=(2.6+3.0*fract(seed*8.1))*mass*sin(pow(dp,0.65)*3.14159);",
    "        vec2 diff=px-vec2(dx,dy);",
    "        diff.y*=(diff.y<0.0)?0.54:0.95;",
    "        float blob=clamp(1.0-length(diff)/max(rad*2.15,0.001),0.0,1.0);",
    "        dropField=smax(dropField,blob*0.96,0.18);",
    "      }",
    "    }",
    "  }",
    "  float combined=smax(letterField,pourField,0.16*smoothstep(0.0,0.15,lp));",
    "  combined=smax(combined,dropField,0.18*smoothstep(0.05,0.25,lp));",
    "  combined*=(1.0-smoothstep(0.88,0.995,p));",
    "  float washNoise=0.48+0.62*n2;",
    "  float washEnv=sin(clamp(p*1.04,0.0,1.0)*3.14159)*(1.0-smoothstep(0.82,0.99,p));",
    "  float washAlpha=smoothstep(0.14,0.60,streakWash*washNoise)*washEnv*0.38;",
    "  float fw=max(fwidth(combined),0.016);",
    "  float cutoff=mix(0.49,0.45,smoothstep(0.0,0.2,lp));",
    "  float solidAlpha=smoothstep(cutoff-fw,cutoff+fw,combined);",
    "  float finalAlpha=clamp(max(solidAlpha,washAlpha),0.0,1.0);",
    "  if(finalAlpha<0.004)discard;",
    "  vec3 deepInk=vec3(0.30,0.00,0.82);",
    "  vec3 brandViolet=vec3(0.4627,0.0078,1.0);",
    "  vec3 vividOrchid=vec3(0.76,0.10,1.00);",
    "  vec3 magentaBleed=vec3(1.00,0.204,0.953);",
    "  float wetMix=smoothstep(0.02,0.20,p);",
    "  float thickness=clamp((combined-0.43)/0.42,0.0,1.0);",
    "  float flowTint=clamp((yDist/95.0)*0.50*wetMix,0.0,0.48);",
    "  vec3 wetCol=mix(magentaBleed,vividOrchid,smoothstep(0.0,0.36,thickness));",
    "  wetCol=mix(wetCol,brandViolet,smoothstep(0.28,0.74,thickness)*(1.0-flowTint));",
    "  wetCol=mix(wetCol,mix(deepInk,vec3(0.94,0.89,1.0),u_dark*0.78),smoothstep(0.72,1.0,thickness));",
    "  vec2 grad=vec2(dFdx(combined),dFdy(combined));",
    "  vec3 norm=normalize(vec3(-grad*18.0,1.0));",
    "  float spec=pow(max(dot(norm,normalize(vec3(-0.42,-0.68,0.60))),0.0),20.0)*wetMix*solidAlpha*0.42;",
    "  vec3 bodyCol=mix(u_baseCol,wetCol,wetMix);",
    "  vec3 washCol=mix(brandViolet,magentaBleed,clamp(0.30+0.70*n1,0.0,1.0));",
    "  vec3 col=mix(washCol,bodyCol,clamp(solidAlpha/max(finalAlpha,0.001),0.0,1.0));",
    "  col+=vec3(0.96,0.88,1.0)*spec;",
    "  gl_FragColor=vec4(col,finalAlpha);",
    "}"
  ].join("\n");

  function parseRGB(str) {
    var m = str && str.match(/(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)/);
    if (!m) return [0.4627, 0.0078, 1.0];
    return [parseFloat(m[1]) / 255, parseFloat(m[2]) / 255, parseFloat(m[3]) / 255];
  }

  function buildTexture(cb) {
    var scale = 3;
    var w = CV_W * scale;
    var h = CV_H * scale;
    var img = new Image();
    img.onload = function () {
      function layer(blurPx) {
        var c = document.createElement("canvas");
        c.width = w;
        c.height = h;
        var ctx = c.getContext("2d");
        if (blurPx > 0 && "filter" in ctx) ctx.filter = "blur(" + blurPx * scale + "px)";
        ctx.drawImage(img, PAD.left * scale, PAD.top * scale, BASE_W * scale, BASE_H * scale);
        return ctx.getImageData(0, 0, w, h).data;
      }
      var sharp = layer(0);
      var tight = layer(2.0);
      var med = layer(4.8);
      var wide = layer(10.0);

      var out = document.createElement("canvas");
      out.width = w;
      out.height = h;
      var octx = out.getContext("2d");
      var outImg = octx.createImageData(w, h);
      var od = outImg.data;
      for (var i = 0, n = w * h; i < n; i++) {
        var idx = i * 4;
        od[idx] = sharp[idx + 3];
        od[idx + 1] = tight[idx + 3];
        od[idx + 2] = med[idx + 3];
        od[idx + 3] = wide[idx + 3];
      }
      octx.putImageData(outImg, 0, 0);
      cb(out);
    };
    img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(SVG_MARKUP);
  }

  function initEngine() {
    if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    buildTexture(function (texCanvas) {
      var canvas = document.createElement("canvas");
      canvas.className = "roasist-ink-canvas";
      canvas.setAttribute("aria-hidden", "true");
      canvas.style.cssText =
        "position:absolute;pointer-events:none;opacity:0;visibility:hidden;z-index:2;will-change:opacity;";

      var dpr = Math.min(window.devicePixelRatio || 1, 2.5);
      if (dpr < 2) dpr = 2;
      canvas.width = Math.round(CV_W * dpr);
      canvas.height = Math.round(CV_H * dpr);

      var gl =
        canvas.getContext("webgl", { alpha: true, premultipliedAlpha: false, antialias: true }) ||
        canvas.getContext("experimental-webgl", { alpha: true, premultipliedAlpha: false, antialias: true });
      if (!gl) return;
      gl.getExtension("OES_standard_derivatives");

      function compile(type, src) {
        var s = gl.createShader(type);
        gl.shaderSource(s, src);
        gl.compileShader(s);
        if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
          gl.deleteShader(s);
          return null;
        }
        return s;
      }

      var vs = compile(gl.VERTEX_SHADER, VS);
      var fs = compile(gl.FRAGMENT_SHADER, FS);
      if (!vs || !fs) return;

      var prog = gl.createProgram();
      gl.attachShader(prog, vs);
      gl.attachShader(prog, fs);
      gl.linkProgram(prog);
      if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return;
      gl.useProgram(prog);

      var buf = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, buf);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]), gl.STATIC_DRAW);
      var aPos = gl.getAttribLocation(prog, "a_pos");
      gl.enableVertexAttribArray(aPos);
      gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);

      var tex = gl.createTexture();
      gl.bindTexture(gl.TEXTURE_2D, tex);
      gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, false);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, texCanvas);

      var uProg = gl.getUniformLocation(prog, "u_progress");
      var uDark = gl.getUniformLocation(prog, "u_dark");
      var uBaseCol = gl.getUniformLocation(prog, "u_baseCol");
      var uRes = gl.getUniformLocation(prog, "u_res");
      var uRect = gl.getUniformLocation(prog, "u_logoRect");

      gl.viewport(0, 0, canvas.width, canvas.height);
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

      var mounted = false;
      var progress = window.scrollY > 40 ? 1.0 : 0.0;
      var target = progress;
      var rafId = 0;
      var lastTs = 0;

      function getRefs() {
        var header = document.querySelector(".Header_header__KwdYD");
        var logo = header && header.querySelector(".Header_logo____uDV");
        var svg = logo && logo.querySelector("svg");
        return { header: header, logo: logo, svg: svg };
      }

      function syncLayout(refs) {
        if (!refs.header || !refs.svg) return false;
        if (!mounted || canvas.parentNode !== refs.header) {
          refs.header.appendChild(canvas);
          mounted = true;
        }
        var hRect = refs.header.getBoundingClientRect();
        var sRect = refs.svg.getBoundingClientRect();
        if (sRect.width < 10) return false;
        var scale = sRect.width / BASE_W;
        canvas.style.width = CV_W * scale + "px";
        canvas.style.height = CV_H * scale + "px";
        canvas.style.left = sRect.left - hRect.left - PAD.left * scale + "px";
        canvas.style.top = sRect.top - hRect.top - PAD.top * scale + "px";
        return true;
      }

      function applyStateClasses() {
        if (!document.body) return;
        document.body.classList.add("roasist-ink-ready");
        if (progress <= 0.002) {
          document.body.classList.remove("roasist-ink-running", "roasist-ink-hidden");
          canvas.style.opacity = "0";
          canvas.style.visibility = "hidden";
        } else if (progress >= 0.998) {
          document.body.classList.remove("roasist-ink-running");
          document.body.classList.add("roasist-ink-hidden");
          canvas.style.opacity = "0";
          canvas.style.visibility = "hidden";
        } else {
          document.body.classList.add("roasist-ink-running");
          document.body.classList.remove("roasist-ink-hidden");
          canvas.style.opacity = "1";
          canvas.style.visibility = "visible";
        }
      }

      function drawFrame(p, refs) {
        var isDark = document.body && document.body.classList.contains("dark") ? 1.0 : 0.0;
        var rgb = refs.logo ? parseRGB(window.getComputedStyle(refs.logo).color) : [0.4627, 0.0078, 1.0];
        // Smoothly ease visual progress so both forward melt and reverse reform feel fluid & viscous
        var eased = p < 0.5 ? 2.0 * p * p : 1.0 - Math.pow(-2.0 * p + 2.0, 2.0) / 2.0;
        var visualP = 0.35 * p + 0.65 * eased;

        gl.clearColor(0, 0, 0, 0);
        gl.clear(gl.COLOR_BUFFER_BIT);
        gl.uniform1f(uProg, visualP);
        gl.uniform1f(uDark, isDark);
        gl.uniform3f(uBaseCol, rgb[0], rgb[1], rgb[2]);
        gl.uniform2f(uRes, CV_W, CV_H);
        gl.uniform4f(uRect, PAD.left / CV_W, PAD.top / CV_H, BASE_W / CV_W, BASE_H / CV_H);
        gl.drawArrays(gl.TRIANGLES, 0, 6);
      }

      function tick(ts) {
        if (!lastTs) lastTs = ts;
        var dt = Math.min((ts - lastTs) / 1000, 0.05);
        lastTs = ts;

        var speed = target > progress ? 1 / 1.05 : 1 / 0.92;
        if (Math.abs(target - progress) <= speed * dt) {
          progress = target;
        } else {
          progress += (target > progress ? 1 : -1) * speed * dt;
        }

        var refs = getRefs();
        if (progress > 0.002 && progress < 0.998) {
          if (syncLayout(refs)) {
            drawFrame(progress, refs);
          }
        }
        applyStateClasses();

        if (Math.abs(target - progress) > 0.0005) {
          rafId = window.requestAnimationFrame(tick);
        } else {
          rafId = 0;
          lastTs = 0;
        }
      }

      function updateTarget() {
        var scrolled = window.scrollY > 40;
        if (document.body) {
          if (scrolled) document.body.classList.add("roasist-scrolled");
          else document.body.classList.remove("roasist-scrolled");
        }
        var nextTarget = scrolled ? 1.0 : 0.0;
        if (nextTarget !== target) {
          target = nextTarget;
          if (!rafId) {
            lastTs = 0;
            rafId = window.requestAnimationFrame(tick);
          }
        }
      }

      // Mount safely after hydration settles (or on first scroll)
      function safeBoot() {
        progress = window.scrollY > 40 ? 1.0 : 0.0;
        target = progress;
        var refs = getRefs();
        syncLayout(refs);
        applyStateClasses();
      }

      if (document.readyState === "complete") {
        setTimeout(safeBoot, 320);
      } else {
        window.addEventListener("load", function () {
          setTimeout(safeBoot, 320);
        });
      }

      window.addEventListener("scroll", updateTarget, { passive: true });
      window.addEventListener(
        "resize",
        function () {
          var refs = getRefs();
          syncLayout(refs);
          if (progress > 0.002 && progress < 0.998) drawFrame(progress, refs);
        },
        { passive: true }
      );
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initEngine);
  } else {
    initEngine();
  }
})();
