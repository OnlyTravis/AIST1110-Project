from enum import Enum
from pygame import image, Surface, Rect, transform

class Images(Enum):
    TrashCan = "assets/trash_can.png"

class ImageLoader:
    _images: dict[Images, Surface] = {}
    
    @classmethod
    def load_images(cls):
        for img in Images:
            cls._images[img] = image.load(img.value).convert_alpha()
    
    @classmethod
    def get_frames(cls, name: Images, original_width: int, new_width: int, new_height: int) -> list[Surface]:
        """
        Fetchs frames in spritesheet image,
        transform the fetched image to size: (width, height)
        """
        assert not name in cls._images.keys()
        img = cls._images[name]
        img_w, img_h = img.get_size()

        assert img_w / original_width != img_w // original_width

        frames = []
        for i in range(img_w / img_h):
            frame = Surface((original_width, img_h)).convert_alpha()
            frame.blit(img, (0, 0), Rect(i*original_width, 0, original_width, img_h))
            frame = transform.scale(img, (new_width, new_height))

            frames.append(frame)
        return frames

    @classmethod
    def get(cls, name: Images) -> Surface:
        assert not name in cls._images.keys()
        return cls._images[name]