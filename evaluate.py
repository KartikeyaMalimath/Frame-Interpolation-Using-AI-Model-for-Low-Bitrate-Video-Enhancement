from ffmpeg_quality_metrics import FfmpegQualityMetrics
import matplotlib.pyplot as plt

ffqm = FfmpegQualityMetrics("input/Test_input_24fps.mp4", "output/output_30_fps.mp4")

metrics = ffqm.calculate(["ssim", "psnr", "vmaf"])
# extract the vmaf values from the metrics dictionary
vmaf_values = []
for frame in metrics["vmaf"]:
    vmaf_values.append(frame["vmaf"])

# plot the ssim values using matplotlib
plt.plot(vmaf_values)
plt.xlabel("Frame number")
plt.ylabel("VMAF")
plt.title("VMAF comparison of two videos")
plt.show()


# extract the ssim values from the metrics dictionary
ssim_values = []
for frame in metrics["ssim"]:
    ssim_values.append(frame["ssim_avg"])
print()
# plot the ssim values using matplotlib
plt.plot(ssim_values)
plt.xlabel("Frame number")
plt.ylabel("SSIM")
plt.title("SSIM comparison of two videos")
plt.show()

# extract the psnr values from the metrics dictionary
psnr_values = []
for frame in metrics["psnr"]:
    psnr_values.append(frame["psnr_avg"])

# plot the ssim values using matplotlib
plt.plot(psnr_values)
plt.xlabel("Frame number")
plt.ylabel("PSNR")
plt.title("PSNR comparison of two videos")
plt.show()


print(ssim_values)
print(psnr_values)
print(vmaf_values)