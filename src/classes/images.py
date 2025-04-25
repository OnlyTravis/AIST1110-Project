from enum import Enum
from pygame import image, Surface, Rect, transform, SRCALPHA

class Images(Enum):
    TrashCan = "assets/trash_can.png"
    Letter = "assets/letter.png"
    SubmitButton = "assets/submit_button.png"

class ImageLoader:
    _images: dict[Images, Surface] = {}
    
    @classmethod
    def load_images(cls):
        for img in Images:
            cls._images[img] = image.load(img.value).convert_alpha()
    
    @classmethod
    def get_frames(cls, name: Images, segment_width: int, new_width: int, new_height: int) -> list[Surface]:
        """
        Fetchs frames in spritesheet image,
        transform the fetched image to size: (width, height)
        """
        assert name in cls._images.keys()
        img = cls._images[name]
        img_w, img_h = img.get_size()

        assert img_w / segment_width == img_w // segment_width

        frames = []
        for i in range(int(img_w / segment_width)):
            frame = Surface((segment_width, img_h), SRCALPHA)
            frame.blit(img, (0, 0), Rect(i*segment_width, 0, segment_width, img_h))
            frame = transform.scale(frame, (new_width, new_height)).convert_alpha()

            frames.append(frame.convert_alpha())
        return frames

    @classmethod
    def get(cls, name: Images, w: int=-1, h: int=-1, scale: float=-1) -> Surface:
        """
        Fetchs Image corresponding to Images enum.
        Transforms the image to size (w, h) if both w and h are provided
        Scales the image by the factor "scale" if scale is provided
        (w and h are considered first)
        """
        assert not name in cls._images.keys()
        img = cls._images[name]

        if w != -1 and h != -1:
            return transform.scale(img, (w, h))
        
        if scale != -1:
            return transform.scale_by(img, scale)

        return img