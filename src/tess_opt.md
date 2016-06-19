# Making Faster Fragment Shaders by Using Tessellation Shaders

In order to fully understand this post, it is necessary that you understand
the following topics:

* Basic usage of Tessellation Shaders. You can study this topic [here](http://ogldev.atspace.co.uk/www/tutorial30/tutorial30.html) and [here](http://ogldev.atspace.co.uk/www/tutorial31/tutorial31.html)
* Barycentric Coordinates. You can study this topic [here](http://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/barycentric-coordinates)
* Perlin Noise and Simplex Noise. You can study this topic [here.](http://webstaff.itn.liu.se/~stegu/simplexnoise/simplexnoise.pdf)

So I will be making the assumption that the reader is knowledgeable in these topics.

## Introduction

In the paper [Automatic Shader Simplification using Surface Signal
Approximation](http://www.cad.zju.edu.cn/home/bao/pub/36.pdf), Wang et
al described an algorithm that does automatic shader
simplification. Put briefly, the algorithm automatically rewrites
shaders so that they become much, much faster. They are using several
techniques to achieve this, and one of those techniques I'd like to
described in this post. The technique is that they are moving
expensive operations from a fragment shader into some earlier shader
stage, and by doing so they greatly reduce the number of times said
operation has to be evaluated. In this article, I shall in much detail
describe this technique.

## Explaining the Main Idea

So, let us say that we have a shader with fragment shader that is very
expensive(we are focusing our efforts in simplifying the fragment
shader, because it is the shader stage that tends to be the most
expensive nowadays).  Now, how could we make this shader less
expensive? One way of achieveing a speedup, is that we simplify try to
run the fragment shader less. The main reason that a fragment shader
is expensive, is because it has to be evaluated for every single
fragment that the geometry covers.

But is it really to evaluate it for every single fragment? Maybe it
could be enough to evaluate it for the vertices of the geometry, and
then in the fragment shader we interpolate between the values computed at
the vertices? Let us try that idea out! So, let us try optimizing the
following shader:

```glsl
//
// Vertex Shader
//
layout(location = 0) in vec3 vsPos;
layout(location = 1) in vec3 vsNormal;

out vec3 fsPos;
out vec3 fsNormal;

uniform mat4 uMvp;

void main()
{
    fsPos = vsPos;
    fsNormal = vsNormal;

    gl_Position = uMvp * vec4(vsPos, 1.0);
}

//
// Fragment Shader
//
in vec3 fsPos;
in vec3 fsNormal;

out vec3 color;

uniform mat4 uView;

void main()
{
    color = doSpecularLight(fsNormal, fsPos, uView);
}

```

where the function `doSpecularLight` simply does a standard specular
light calculation. And since we are calling this function in the
fragment shader, that means that the function will be evaluated for
every single fragment that the geometry covers. If `doSpecularLight`
were expensive to evaluate, it would certainly be very expensive to
evaluate it for every single fragment.

If we apply the above shader on a teapot, the result is the following:

<img src="../img/tess_opt/spec_frag.png" width="425" height="390"
alt="Specular Calculation in the Fragment Shader"
title="Specular Calculation in the Fragment Shader"
/>


Let us now try the idea that I mentioned above; let us move that
specular calculation from the fragment shader to the vertex shader. So
we essentially move code from the fragment shader to the vertex
shader:

![Pipeline1](../img/tess_opt/pipeline1.png "Pipeline1")

So let us do that to the shader:

```glsl
//
// Vertex Shader
//
layout(location = 0) in vec3 vsPos;
layout(location = 1) in vec3 vsNormal;

out vec3 fsResult;

uniform mat4 uMvp;

void main()
{
    fsResult = doSpecularLight(vsNormal, vsPos, uView);

    gl_Position = uMvp * vec4(vsPos, 1.0);
}



//
// Fragment Shader
//
in vec3 fsResult;

out vec3 color;

void main()
{
    color = fsResult;
}

```

So now we are calling `doSpecularLight` in the vertex shader, and then
sending the result to the fragment shader. The value that is received
by the fragment shader, is calculated by hardware by interpolating
between the three vertices that are closest to the fragment(this
interpolation is based on barycentric coordinates, and you can more
about this
[here](http://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/barycentric-coordinates)
).

So the resulting specular lighting is not true fragment shader
specular lighting. Rather, we are trying to approximate the fragment
shader specular lighting by interpolating between the values at the
vertices. However, since we are not computing the specular lighting
for every single fragment, but for only the vertices, the resulting
shader should be much cheapter


How does this new shader look? Like this:

![Specular Calculation in the vertex Shader](../img/tess_opt/spec_vert.png "Specular Calculation in the vertex Shader")

As can be observed, doing the calculation in the vertex shader results
in a noticeable drop in quality; the specular highlight is longer
round, but a has a slightly blocky appearance at the borders. And we
can see some obvious banding artifacts.

Why do we obtain such an horrendous result? The main problem is that
the specular lighting generates a relatively high frequency signal, and if take
too few samlpes, we will not be able to approximate this signal by
just using barycentric interpolation. In our case, the samples are
taken at every vertex. And how many vertices does our teapot model have?
Let us render it as wireframe:

![Teapot Wireframe Level 1](../img/tess_opt/teapot_wireframe1.png "Teapot
 Wireframe Level 1")

Now, look at the vertex density at the location where the big
highlight was rendered. As can be observed, the vertex is not very high, and thus the
number of samples will be to low to approximate the original signal.

So if want a better result, we need to take more samples. Wang et
al. came up with a elegant and ingenious solution to this problem: we
simply use a tessellation shader to subdivide the triangles of the
mesh into subtriangles! By doing so, the vertex density of the model
will be increased, and so, we can compute even more samples at the
vertices and calculate a better approximation!

## Tessellation Shaders

I will now explain how the idea of Wang et al. can be implemented in
OpenGL using tessellation shaders.

As has already been stated, we will divide all triangles of the
original mesh into subtriangles, and by doing so increase the vertex
density. Wang et al. define the following tessellation levels in the
[supplementary document](http://www.cad.zju.edu.cn/home/rwang/projects/shader-optimization/14shaderopt_supp.pdf) they provided:

![Tessellation Levels](../img/tess_opt/tess_levels.png "Tessellation
 Levels")

So basically, for tessellation level one, we do not subdivide the
triangles at all, but let them be. But for level 2, we add four extra
vertices and subdivide the triangle into six triangles, and so on.

It turns out that this kind of subdivision is surprisingly easy to
implement using tessellation shaders. To do this in OpenGL, first we
need to add two new shader stages: the Tessellation Control Shader,
and the Tessellation Evaluation Shader(hereafter abbreviated TCS and
TES). If we add these two stages, our shader pipeline will look like this:

![Pipeline2](../img/tess_opt/pipeline2.png "Pipeline2")

So, we add the two new shader stages between the vertex and fragment
shaders. Furthermore, the specular calculation is no longer moved from
the fragment shader to the vertex shader, but from fragment to
TES. This is because we do not have access to all vertices in the
vertex shader. In particular, we only have access to the vertices
created through tessellation in TES, and so we must move the specular
calculation to TES.

Now, I shall go through what our new shader looks like. First the
vertex shader:

```glsl
layout(location = 0) in vec3 vsPos;
layout(location = 1) in vec3 vsNormal;

out vec3 tcsPos;
out vec3 tcsNormal;

void main(){
	tcsPos = vsPos;
	tcsNormal = vsNormal;
}
```

We will not be doing the specular calculation in the vertex shader
anymore, so it is simply a pass-though shader now. Next, let us look
at TCS:

```glsl
in vec3 tcsPos[];
in vec3 tcsNormal[];

layout(vertices=3) out; // (1)
out vec3 tesPos[];
out vec3 tesNormal[];

uniform float uTessLevel;

void main(){

    // (2)
    tesNormal[gl_InvocationID] = tcsNormal[gl_InvocationID];
    tesPos[gl_InvocationID] = tcsPos[gl_InvocationID];

    // (3)
    gl_TessLevelOuter[0] = uTessLevel;
    gl_TessLevelOuter[1] = uTessLevel;
    gl_TessLevelOuter[2] = uTessLevel;

    // (4)
    gl_TessLevelInner[0] = uTessLevel;
}
```

The above will need some explanation. I will explained the marked
section of the code. In `(1)` we specify the patch size. The TCS takes
a list of patches, and does subdivision on them. Since in our case
`vertices=3`, we have that the patches are simply the triangles of the
original mesh.

To every vertex of the patch, we associate a normal and a position,
which is what we are doing in `(2)`.

Next, we need to specify tessellation pattern for the
mesh. `gl_TessLevelOuter[0]` specifies how many subedges we should
divide the 0:th edge into. So in `(3)` we are specifying that every
single edge of every single triangle should be subdivided into
`uTessLevel` subedges. Also, note that if `uTessLevel=1`, then no
subdivision will be done at all.

Finally, in `(4)`, we are specifying how many times we should
subdivide the inner part of the triangle.

It should now be clear that if `uTessLEvel=2`, then every triangle
will be subdivided according to tessellation level 2 I showed in the
image above.

That was the TCS. Next comes the TES

```glsl
layout(triangles,equal_spacing) in;
in vec3 tesPos[];
in vec3 tesNormal[];

out vec3 outColor;

uniform mat4 uMvp;
uniform mat4 uView;

vec3 lerp3D(vec3 v0, vec3 v1, vec3 v2)
{
    return vec3(gl_TessCoord.x) * v0 + vec3(gl_TessCoord.y) * v1 + vec3(gl_TessCoord.z) * v2;
}

void main(){
    vec3 pos = lerp3D(tesPos[0],tesPos[1],tesPos[2]);
    vec3 normal = lerp3D(tesNormal[0], tesNormal[1], tesNormal[2]);

    gl_Position = uMvp* vec4(pos, 1.0 );

    fsColor = doSpecularLight(normal, pos, uView);
}

```

This one is a bit more difficult to understand. First, look at this image:

![TES](../img/tess_opt/tes.png "TES")

This is a triangle that has been tessellated to level 2. The yellow
circles are of the three vertices of the original patch(triangle), and
the positions of these vertices are contained in the input array
`tesPos`, and their normals are in `tesNormal`.

These positions and normals we already know. However, by the TCS 4 new
vertices were created(they are the pink circles in the image), and we
do not yet know their positions nor their normals. Kindly enough,
however, the barycentric coordinates of the vertices created through
tesselation are sent to the TES. They are `(gl_TessCoord.x,
gl_TessCoord.y, gl_TessCoord.z)`. For instance, the barycentric
coordinates of the center vertex in the above image will be
`(1/3,1/3,1/3)`.

But we can just use these barycentric coordinates to compute the
positions and normals from `tesPos` and `tesNormal`(this makes sense,
because recall that barycentric coordinates allow us to perform
interpolation on a triangle.).

To summarize, all that the line  `vec3 pos =
lerp3D(tesPos[0],tesPos[1],tesPos[2]);` does that it performs
barycentric interpolation to obtain the positions of all the vertices
on the tessellated triangle.

Now, note that all the vertices, including the ones created through
tessellation, will pass through TES. Thus, it is in shader stage, and
not the vertex shader stage, that we compute the specular
lighting.

Now all that remains is the fragment shader:

```glsl
in vec3 fsColor;

out vec3 color;

void main(){
    color = fsColor;
}
```

After running TCS and TES, the mesh will now consist of many triangles
created through tessellation. And every vertex will have a specular
value associated with it(this was calculated in the end of TES). Now,
the fragment will be contained in exactly one such triangle, and the
specular value outputted by the fragment shader will be computed by
interpolating between the specular values at the vertices of said
triangle. Since the tessellation has increased the vertex density,
this should result in a much better approximation of the original
fragment shader specular lighting.

How much better does this look? Here is the result for tessellation
level 1:

![Specular Lighting Tessellation Level
 1](../img/tess_opt/spec_tess1.png "Specular Lighting Tessellation
 Level 1")

But for tessellation level 1 we are not doing any tessellation at all,
so we get the same results are we did when we were doing the
calculation for every vertex. So let us try level 2

![Specular Lighting Tessellation Level
 2](../img/tess_opt/spec_tess2.png "Specular Lighting Tessellation
 Level 2")

This already looks much better! And note that level 2 has 6 times as
many triangles as level 2. Below we can see the difference in vertex density.

![Tessellation Level Comparison](../img/tess_opt/tess_level_compare.png "Tessellation Level Comparison")


But tessellation level 2 still have some very slight banding
artifacts. But by increasing the level to 3, that problem pretty much
goes away:

![Specular Lighting Tessellation Level
 3](../img/tess_opt/spec_tess3.png "Specular Lighting Tessellation
 Level 3")

Let us now compare level 3 with the original fragment shader specular:

![Specular Lighting Original Vs Level
 3](../img/tess_opt/compare_level3_original.png "Specular Lighting
 Original Vs Level 3")

As can be observed, the approximation is now almost perfect! But the
tessellated version should be much faster, since it does not compute
the specular lighting for every single fragment!

## Speeding up Procedural Textures

So by doing the above are able to speedup a specular lighting
calculation. However, that is a very silly example, because specular
is not at all expensive to compute, even if we are doing it for every
single fragment. So let us instead speedup a more expensive type of
shader: Procedural Texture Shader. A procedural texture shader uses
a Simplex/Perlin noise to compute a texture in real-time, in the
fragment shader. One advantage of such a texture is that it is very
easy to make such a texture tile. But one disadvantage is that it is
quite expensive to calculate a texture in real-time. But by using the
technique described by Wang et al., we may be able to solve that
problem.

In our case, the texture will be created by adding 4 octaves of
Simplex noise. When applied to the teapot, the texture looks like this:

![Original Procedural Texture](../img/tess_opt/tex_original.png
 "Original Procedural Texture")

in the above image, the texture is being computed for every single
fragment, using the fragment position as input to the noise
function. But this is quite expensive, so let us test whether we can
approximate the texture by moving that texture calculation from the
fragment shader to the TES. We can see the result in the below montage:

![Procedural Texture Tessellation
 Montage](../img/tess_opt/tex_tess_montage.png
 "Procedural Texture Tessellation Montage")



|            | Intel Iris    | GTX 960       |
-------------| ------------- | ------------- |
**Original** | 0.3232ms      | 0.323ms       |
**Level 1**  | 2.2ms         | 12.1ms       |
**Level 2**  | 2.2ms         | 12.1ms       |
**Level 3**  | 2.2ms         | 12.1ms       |
**Level 4**  | 2.2ms         | 12.1ms       |
**Level 5**  | 2.2ms         | 12.1ms       |
