xquery version "3.1";
declare namespace local = "http://perseus.tufts.edu";

declare namespace output = "http://www.w3.org/2010/xslt-xquery-serialization";
declare option output:method "json";
declare option output:media-type "application/json";


<images>{
let $artifact-images := collection('/db/data/perseus/aa')//ArtifactImg/img
for $i in $artifact-images
let $imageNameRec := collection('/db/data/perseus/aa')//ImageNames/image[archive_number = $i/archive_number]
let $name := $imageNameRec/name/text()
let $name2 := $imageNameRec/secondary_name/text()
let $name3 := $imageNameRec/tertiary_name/text()
let $id := normalize-space(substring-after($i/archive_number, 'Perseus:image:'))


return
 <img>
  <id>{$id}</id>
  {$i/archive_number}
   {if ($name) then
    for $n in $name
     return
      <name>{normalize-space($n)}</name>
      else ()
      }
   {if ($name2) then
    for $n in $name2 return
   <name>{normalize-space($n)}</name>
   else ()
   }
   {if ($name3) then
   for $n in $name3 return
   <name>{normalize-space($n)}</name>
   else ()
   }
   
  {$i/caption}
  {$i/credits}
 </img>
}</images>