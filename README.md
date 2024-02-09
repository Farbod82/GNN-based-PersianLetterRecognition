## Persian Character Recognition using GNN

This started as a project last summar. Persian language is really complicated and open-source OCR applications for our language are limited. I thought maybe using graphs might be the solution. 
I started by watching this great Stanford University course about graphs[https://www.youtube.com/watch?v=JAB_plj2rbA&list=PLoROMvodv4rPLKxIpqhjhPgdQy7imNkDn].
I first ran a classification test on single Letters with a really small dataset. To improve the model I found the paper[https://www.sciencedirect.com/science/article/abs/pii/S003132031400274X]
that used similarity learning with Graph Edit Distances and so I implemented it with the help of this git repository[https://github.com/priba]. This project is still underwork and not complete !


# Preprocessing 
First the image is skeletonized and and then a graph is formed from the character each node being a keypoint of the letter and node values being normalized x and y of the points in the image.

<table>
  <tr>
    <td>
      <img src="image_utility/1.png" alt="Image 1">
    </td>
    <td>
      Data Sample
    </td>
  </tr>
  <tr>
      <td>
      <img src="image_utility/2.png" alt="Image 2">
      </td>
      <td>
        Skeletonized
      </td>
   </tr>
     <tr>
      <td>
      <img src="image_utility/3.png" alt="Image 3">
      </td>
      <td>
        Graph
      </td>
   </tr>
</table>




