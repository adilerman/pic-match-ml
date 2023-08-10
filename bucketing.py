"""
Algorithm:
    1. compare all images.
    2. save all matching pairs.
    3. create all cliques.
    4. find the biggest cliques, add images to it. by democracy.
        4.1. save group to bucket.
    5. back to 4. for second-largest group and remaining images. and so on.

"""
import itertools

from common.utils import filter_nested_lists
from image_comparer import ImageComparer
from my_image import MyImage
from glob import glob

CLIQUE_EXPAND_THRESHOLD = 4


def get_all_pairs(lst):
    return list(itertools.combinations(lst, 2))


def get_matches_by_image(all_matches, image_path):
    res = []
    for img_path1, img_path2 in all_matches:
        if img_path1 == image_path:
            res.append(img_path2)
        if img_path2 == image_path:
            res.append(img_path1)
    return res


def get_graph_cliques(matches, all_images_paths):
    unstructured_cliques = find_cliques(matches, remaining_images=all_images_paths)
    cliques = filter_nested_lists(unstructured_cliques, result=[])
    return cliques


def find_cliques(all_matches, potential_clique=[], remaining_images=[], skip_images=[]):
    if len(remaining_images) == 0 and len(skip_images) == 0 and len(potential_clique) > 2:
        # print('This is a clique:', potential_clique)
        return potential_clique
    found_cliques = []
    for image_path in remaining_images:
        matches = get_matches_by_image(all_matches, image_path)
        # Try adding the node to the current potential_clique to see if we can make it work.
        new_potential_clique = potential_clique + [image_path]
        new_remaining_images = [n for n in remaining_images if n in matches]
        new_skip_list = [n for n in skip_images if n in matches]
        recursive_res = find_cliques(all_matches, new_potential_clique, new_remaining_images, new_skip_list)
        found_cliques.append(recursive_res) if recursive_res else None
        # We're done considering this img.  If there was a way to form a clique with it, we
        # already discovered its maximal clique in the recursive call above.  So, go ahead
        # and remove it from the list of remaining nodes and add it to the skip list.
        remaining_images.remove(image_path)
        skip_images.append(image_path)
    return found_cliques


class Bucketing:
    def __init__(self, input_path):
        self.image_comparer = ImageComparer()
        self.input_path = input_path
        self.all_images_paths = glob(input_path + ('*jpg' if input_path.endswith('/') else '/*jpg'))

    def find_matching_pairs(self):
        image_pairs = get_all_pairs(self.all_images_paths)
        all_matches = []
        for img1_path, img2_path in image_pairs:
            img1 = MyImage(img1_path)
            img2 = MyImage(img2_path)
            is_matching = self.image_comparer.compare_images(img1, img2, False)
            if is_matching:
                all_matches.append((img1_path, img2_path))
        return all_matches


def create_bucket_for_clique(clique):
    print(f"the following bucket contains {clique}")


def bucket_images(matches, images_to_bucket):
    if not images_to_bucket:
        return
    cliques = get_graph_cliques(matches, all_images_paths=images_to_bucket.copy())
    if not cliques:
        return
    largest_clique = max(cliques, key=len)
    images_to_bucket = [img for img in images_to_bucket if img not in largest_clique]
    # add images to clique
    for image_path in images_to_bucket:
        current_image_matches = get_matches_by_image(matches, image_path)
        matches_in_larges_clique = len([match for match in current_image_matches if match in largest_clique])
        if matches_in_larges_clique >= CLIQUE_EXPAND_THRESHOLD:
            largest_clique.append(image_path)
    # create bucket for the click
    create_bucket_for_clique(largest_clique)
    images_to_bucket = [img for img in images_to_bucket if img not in largest_clique]
    matches = [(img1, img2) for img1, img2 in matches if img1 not in largest_clique and img2 not in largest_clique]
    bucket_images(matches, images_to_bucket)


if __name__ == '__main__':
    bucketing = Bucketing(input_path='./data/images/640x480/')
    all_matches = bucketing.find_matching_pairs()
    bucket_images(all_matches, images_to_bucket=bucketing.all_images_paths)
    x = 4
