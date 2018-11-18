
import markdown2
import datetime

posts = [
    ("src/model_matrix_recover.html", 
	"Recovering the Scale, Rotation and Translation Matrices from the Model Matrix",
	"/img/gallery/trs_model.png", 
	"I will in this post show how to recover the separate translation, scale, and rotation matrices from the model matrix."),

    ("src/hiz_occlusion_culling.html", 
	"Hierarchical Z-buffer Occlusion Culling: A Brief Explanation",
	"/img/gallery/hiz_occlusion_culling.jpg", 
	"A brief explanation of the Hierarchical Z-buffer Occlusion Culling technique."),

    ("src/marrs2018.html", 
	"Explanation of the paper 'View-warped Multi-view Soft Shadows for Local Area Lights'",
	"/img/gallery/marrs2018.png", 
	"I will in this post write down an explanation of the intuition behind the paper 'View-warped Multi-view Soft Shadows for Local Area Lights'."),

    ("src/sorkine2007.html", 
	"Explanation of the paper 'As-Rigid-As-Possible Surface Modeling'",
	"/img/gallery/sorkine2007.png", 
	"I will in this post write down an explanation of the intuition behind the paper 'As-Rigid-As-Possible Surface Modeling'."),

    ("src/kerbl2018_tldr.html", 
	"TL;DR of the paper 'Revisiting The Vertex Cache: Understanding and Optimizing Vertex Processing on the modern GPU'",
	"/img/gallery/kerbl2018_tldr.png", 
	"I will in this post write down a TL;DR of the paper 'Revisiting The Vertex Cache: Understanding and Optimizing Vertex Processing on the modern GPU'"),

    ("src/tokuyoshi2018_tldr.html", "TL;DR of the paper 'Conservative Z-Prepass for Frustum-Traced Irregular Z-Buffers'", "/img/gallery/tokuyoshi2018_tldr.png", "I will in this post write down a TL;DR of the paper 'Conservative Z-Prepass for Frustum-Traced Irregular Z-Buffers'"),

    ("src/urena2018_tldr.html", "TL;DR of the paper 'Stratified Sampling of Projected Spherical Caps'", "/img/urena2018_tldr/img1.jpeg", "I will in this post write down a TL;DR of the paper 'Stratified Sampling of Projected Spherical Caps'"),


    ("src/whelan2018_tldr.html", "TL;DR of the paper 'Reconstructing Scenes with Mirror and Glass Surfaces'", "/img/whelan2018_tldr/img2.png", "I will in this post write down a TL;DR of the paper 'Reconstructing Scenes with Mirror and Glass Surfaces'"),

    ("src/jeruzalski2018_tldr.html", "TL;DR of the paper 'Collision-Aware and Online Compression of Rigid Body Simulations via Integrated Error Minimization'", "/img/jeruzalski2018_tldr/img1.png", "I will in this post write down a TL;DR of the paper 'Collision-Aware and Online Compression of Rigid Body Simulations via Integrated Error Minimization'"),

    ("src/zucker2018_tldr.html", "TL;DR of the paper 'Cube-to-sphere projections for procedural texturing and beyond'", "/img/zucker2018_tldr/img1.png", "I will in this post write down a TL;DR of the paper 'Cube-to-sphere projections for procedural texturing and beyond'"),

    ("src/hole_filling.html", "Smoothly Filling Holes in 3D meshes using Variational Calculus and Surface Fairing", "/img/gallery/bunnymontage.jpg", "In this article, we describe an approach to smoothly filling holes in broken meshes that is based on variational calculus. However, do note that it is not assumed that the reader has experience in variational calculus, and we will instead introduce the necessary concepts from this topic when they are needed"),

    ("src/poisson_blending.html", "An Intuitive Explanation of using Poisson Blending for Seamless Copy-and-Paste of Images", "/img/gallery/kitten_library.jpg", "In this article, we explain the intuition behind an image processing technique called Poisson Blending. This technique is an image processing operator that allows the user to insert one image into another, without introducing any visually unappealing seams."),

    ("src/fast_triangle_rasterization.html", "A Simple, and Trivially Parallelizable Triangle Rasterization Approach", "/img/gallery/tri_rasterization.png", "In this article, a triangle rasterization algorithm that is easy to implement, yet trivial to parallelize is described."),


    ("src/junior_graphics_programmer_interview.html", "Interviewing for your First Job as a Graphics Programmer: a Checklist of Common Interview Questions", "/img/gallery/graphics_interview.jpg", "I have recently been interviewing at game companies, trying to land a job as a junior graphics programmer. Having done so, I gained knowledge of what skills game companies expect of a newly graduated graphics programmer, and what questions they are likely to ask during interviews. I will in this article compile these findings into a handy checklist. "),

    ("src/gauss_newton.html", "Simple Curve Fitting with the Gauss-Newton Algorithm", "img/gauss_newton/plot_karis.png", "It is shown how the Gauss-Newton Algorithm can be used to perform simple curve fitting."),

    ("src/gauss_seidel_graph_coloring.html", "Parallelizing the Gauss-Seidel Method using Graph Coloring", "/img/gallery/complex_graph.png", "In a previous article, we introduced the Jacobi and Gauss-Seidel methods, which are iterative methods for solving linear systems of equation. Specifically, we noted that the Gauss-Seidel method will in general converge towards a solution much quicker than the Jacobi method. The main issue with the Gauss-Seidel method is that it is non-trivial to make into a parallel algorithm. However, it turns out that for a certain class of matrices, it is pretty simple to implement a parallel Gauss-Seidel method."),

    ("src/quaternion_rotation.html", "Showing the Correctness of Quaternion Rotation", "/img/gallery/crossprod.png", "In this article, we shall provide an algebraic proof that shows that quaternion rotation is correct."),

    ("src/jacobi_and_gauss_seidel.html", "The Gauss-Seidel and Jacobi Methods for Solving Linear Systems", "/img/gallery/jacobi_vs_gauss_seidel.png", "In this article, we shall explain the Jacobi and Gauss-Seidel methods, which are two iterative methods used for solving systems of linear equations. Our main objective is to describe how the Gauss-Seidel method can be made into a highly parallel algorithm, thus making it feasable for implementation on the GPU, or even on the CPU using SIMD intrinsics."),

    ("src/area_convex_polygon.html", "Computing the Area of a Convex Polygon", "/img/gallery/polygon_tri.png", "In this article, we shall derive a formula that computes the area of a convex polygon"),

    ("src/masters_thesis.html", "My Master's Thesis: \"Comparing a Clipmap to a Sparse Voxel Octree for Global Illumination\"", "/img/gallery/mtgallery0.jpg", "I describe my master's thesis, give a couple of comments, and provide an image gallery."),

    ("src/cuda_rle.md", "/img/gallery/parle_scatter.png", "In the paper Fine-Grain Parallelization of Entropy Coding on GPGPUs, Ana Balevic describes how Run-length encoding(hereafter abbreviated RLE) can be implemented on the GPU. Although the paper is very sparse on details, I have been able to implement her approach in CUDA."),

    ("src/tess_opt.md", "/img/gallery/tess_opt.jpg", "In the paper Automatic Shader Simplification using Surface Signal Approximation, Wang et al. describes an algorithm that does automatic shader simplification. Put briefly, the algorithm automatically rewrites shaders so that they become much, much faster. They are using several techniques to achieve this, and one of those techniques I'd like to describe in this post."),
]

def get_html_file(md_file):
    return "posts/"+md_file[4:-3] + ".html"

def create_post(input_file):

    with open('src/template.html', 'r') as f:
        template=f.read()

    if input_file[-5:] == '.html':

        with open(input_file, 'r') as f:
            html_source=f.read()

        # process markdown.
        article_src = '<div class="container">' + html_source + '</div>'
        src = template.format(src=article_src)

        output_file = "posts/"+input_file[4:-5] + '.html'

       # print output_file

        with open(output_file, 'w') as f:
            f.write(src)

    else:

        with open(input_file, 'r') as f:
            markdown_source=f.read()

        # process markdown.
        article_src = '<div class="container">' + markdown2.markdown(markdown_source, extras=["fenced-code-blocks","tables"]) + '</div>'

        src = template.format(src=article_src)

        output_file = get_html_file(input_file)

        with open(output_file, 'w') as f:
            f.write(src)
