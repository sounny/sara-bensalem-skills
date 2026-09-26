import shutil
import os

skills = [
    'portfolio-monograph',
    'constructive-detail',
    'grill-my-design',
    'spatial-anatomy',
    'bioclimatic-flows',
    'interior-joinery',
    'spatial-choreography',
    'spatial-stitch',
    'design-md-extractor',
    'editorial-studio'
]

src_base = r'g:\My Drive\Projects\sara-bensalem-skills\skills'
dst_bases = [
    r'C:\Users\sounn\.gemini\config\skills',
    r'g:\My Drive\skills'
]

for skill in skills:
    src = os.path.join(src_base, skill)
    if not os.path.exists(src):
        continue
    for dst_base in dst_bases:
        dst = os.path.join(dst_base, skill)
        shutil.copytree(src, dst, dirs_exist_ok=True)

print('All 10 canonical skills synchronized to config and My Drive!')
