from enum import Enum
from pygame import image, Surface, Rect, transform, SRCALPHA

class Images(Enum):
    TrashCan = "assets/trash_can.png"

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
    def get(cls, name: Images) -> Surface:
        assert not name in cls._images.keys()
        return cls._images[name]