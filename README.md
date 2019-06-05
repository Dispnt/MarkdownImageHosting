# MarkdownImageHosting
Move image in markdown to sm.ms. Support both inline style and reference style. 
迁移markdown内图片至sm.ms图床，微博相册图床可以全部转出来了...
行内式和参考式都可以用嗷

## Usage: 
### single file:<br>
`python MarkdownImage.py [input.markdown] [output.markdown]` <br>
This will move all images form a single file to a specified path<br>
写明输入输出可以迁移单个文件内的图片<br>
### Multiple files:<br>
`python MarkdownImage.py` <br>
不写就会迁移目录内所有 .txt 或 .md 内的 markdown 图片<br>
This will apply all .txt or .md files in the directory to separate *_new.md.
