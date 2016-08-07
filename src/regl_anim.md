# I made some weird animations in WebGL

Using the WebGL framework
[regl](https://github.com/mikolalysenko/regl), I made some weird
animations. All of them are basically  just using trigonometric functions to
create patterns in a fragment shader. Check out the source code if
you are interested.

<script language=javascript src="../script/regl_anim/regl.min.js"></script>

<canvas id="glcanvas1" width="480" height="270">
  Your browser doesn't appear to support the <code>&lt;canvas&gt;</code> element.
</canvas>
<script language=javascript src="../script/regl_anim/vines.min.js"></script>
<script>  vines(initREGL, 'glcanvas1')</script>
<p style="text-align: center"><a href="https://github.com/Erkaman/regl-anim/blob/master/anims/vines.js">Source Code</a></p>

<canvas id="glcanvas2" width="480" height="270">
  Your browser doesn't appear to support the <code>&lt;canvas&gt;</code> element.
</canvas>
<script language=javascript src="../script/regl_anim/rainbow.min.js"></script>
<script>  rainbow(initREGL, 'glcanvas2')</script>
<p style="text-align: center"><a href="https://github.com/Erkaman/regl-anim/blob/master/anims/rainbow.js">Source Code</a></p>

<canvas id="glcanvas3" width="480" height="270">
  Your browser doesn't appear to support the <code>&lt;canvas&gt;</code> element.
</canvas>
<script language=javascript src="../script/regl_anim/circle.min.js"></script>
<script>  circle(initREGL, 'glcanvas3')</script>
<p style="text-align: center"><a href="https://github.com/Erkaman/regl-anim/blob/master/anims/circle.js">Source Code</a></p>
