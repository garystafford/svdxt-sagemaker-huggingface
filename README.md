# Stable Video Diffusion XT 1.1 on Amazon SageMaker

Stability AI's Stable Video Diffusion XT (SVT-XT) 1.1 foundation model is a diffusion model that takes in a still image as a conditioning frame and generates a video from it. This notebook walks through creating an asynchronous inference endpoint to host the SVT-XT foundation model on Amazon SageMaker.

## Wide-format Videos

<table>
   <tr>
      <td><img src="video_samples/red_car_1.gif" alt="Red Sports Car" width="512"/>
      </br><a href="https://www.pexels.com/photo/red-alfa-romeo-c4-on-road-near-trees-210019">Source image</a></td>
      <td><img src="video_samples/beach_bike_2.gif" alt="Motorcycle on Beach" width="512"/>
      </br><a href="https://www.pexels.com/photo/photo-of-man-riding-bicycle-4054069">Source image</a></td>
   </tr>
   <tr>
      <td><img src="video_samples/waterfall_2.gif" alt="Tropical Waterfall" width="512"/>
      </br><a href="https://www.pexels.com/photo/time-lapse-photography-of-waterfall-2406388">Source image</a></td>
      <td><img src="video_samples/boat_ocean_1.gif" alt="Boat on Shore" width="512"/>
      </br><a href="https://www.pexels.com/photo/seinboat-sunrise-20544112">Source image</a></td>
   </tr>
   <tr>
      <td><img src="video_samples/rocket_1.gif" alt="Rocket" width="512"/>
      </br><a href="https://cdn-lfs.huggingface.co/datasets/huggingface/documentation-images/83e7729b516ba725cb2283eb397ec2c77fc4b120f52a83801f610eac353b63c4?response-content-disposition=inline%3B+filename*%3DUTF-8%27%27rocket.png%3B+filename%3D%22rocket.png%22%3B&response-content-type=image%2Fpng&Expires=1713928309&Policy=eyJTdGF0ZW1lbnQiOlt7IkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTcxMzkyODMwOX19LCJSZXNvdXJjZSI6Imh0dHBzOi8vY2RuLWxmcy5odWdnaW5nZmFjZS5jby9kYXRhc2V0cy9odWdnaW5nZmFjZS9kb2N1bWVudGF0aW9uLWltYWdlcy84M2U3NzI5YjUxNmJhNzI1Y2IyMjgzZWIzOTdlYzJjNzdmYzRiMTIwZjUyYTgzODAxZjYxMGVhYzM1M2I2M2M0P3Jlc3BvbnNlLWNvbnRlbnQtZGlzcG9zaXRpb249KiZyZXNwb25zZS1jb250ZW50LXR5cGU9KiJ9XX0_&Signature=pokKCBg3BgH-9jjbWu1DnDc%7EsmHLz09YNgCAhcfgTXSDXJxQUaQ2JoiT7ofYcogeAGYLf%7EJhUAhfY2eDIWdDABVnbO79iTfcxm%7EmadxCU2o4PCXhNW0IvB67Q2G2hWwYL4mzaIVc2ko5PN-jsAMrY-X-XZn2Pt71C9K-E3MpL%7Ea1nprA5c%7EuY1aeE4gAjmAJe337bJrL5DPB2C1cIp0PnZBcZKoNnB3bwkC-y3l%7ENDt8KThha90ULy0qQra6vG4rOaz-Pljhb8INtlubZxkUBTwN2sqoUkDYSByG2pc7kcDqJmhWqaeOT7nUZ5JkhZptoHtWcsdXHey-iWnnlH7JdA__&Key-Pair-Id=KVTP0A1DKRTAX">Source image</a></td>
      <td><img src="videos/skier.webp" alt="Skier" width="512"/>
      </br><a href="https://www.pexels.com/photo/man-using-ski-3193846/">Source image</a></td>
   </tr>
</table>

## Tall-format Videos

<table>
   <tr>
      <td><img src="video_samples/color_smoke_tall_1.gif" alt="Colored Smoke" width="288"/>
      </br><a href="https://www.pexels.com/photo/red-smoke-illustration-604671">Source image</a></td>
      <td><img src="video_samples/smoke_tall_1.gif" alt="Smoke" width="288"/>
      </br><a href="https://www.pexels.com/photo/close-up-of-beer-glass-against-black-background-255483/">Source image</a></td>
   </tr>
   <tr>
      <td><img src="videos/coffee_1.gif" alt="Turkish Coffee" width="256"/>
      </br><a href="https://www.pexels.com/photo/a-shot-of-steaming-pot-with-a-and-glass-with-a-beverage-10351409">Source image</a></td>
      <td><img src="videos/colored_smoke_2.webp" alt="Colored Smoke" width="387"/>
      </br><a href="https://www.pexels.com/photo/red-smoke-illustration-604671/">Source image</a></td>
   </tr>
   <tr>
      <td><img src="videos/neon_ramen_cat.webp" alt="Neon Ramen Car" width="387"/>
      </br><a href="https://www.pexels.com/photo/gato-otaku-19138491//">Source image</a></td>
   </tr>
</table>
</br>

---

_The contents of this repository represent my viewpoints and not of my past or current employers, including Amazon Web Services (AWS). All third-party libraries, modules, plugins, and SDKs are the property of their respective owners._
