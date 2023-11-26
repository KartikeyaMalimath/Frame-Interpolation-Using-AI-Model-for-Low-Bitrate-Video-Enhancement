# Frame Interpolation Using AI-Model for Low Bitrate Video Enhancement

This project explores the use of artificial intelligence (AI) to improve the quality of low bitrate video with large motion. Due to the compression of video to smaller size, often video is reduced to lower bitrate. This can result in a loss of quality. Frame interpolation is the process of generating intermediate frames between existing frames in a video. The project uses the FILM: Frame Interpolation for Large Motion [1] model by Google Research, which is a powerful AI model for frame interpolation. It is specifically designed for videos with large motion, which means that it is better at handling videos where objects are moving quickly or where there is a lot of camera movement.

The project also develops a user interface, which allows users to interact with the software. The interface allows users to select the video that they want to interpolate and the desired level of quality. The software then uses the FILM model to interpolate the video and generate high-quality interpolated images, to form a high bitrate video.
The project evaluates the performance of the software using various metrics and concludes by discussing the limitations of the software and the potential for future work. The limitations of the software include the computational complexity and the need for large datasets. The potential for future work includes the development of software to generate animated videos using image inputs, high-quality slow-motion video from a low-bit rate video and other implementation of the technology.


### User Input video at 8 FPS


https://github.com/KartikeyaMalimath/Frame-Interpolation-Using-AI-Model-for-Low-Bitrate-Video-Enhancement/assets/37095980/fadc588d-1feb-4d4c-9ea9-bb27ba3f4e92


### Interpolated output video at 30 fps


https://github.com/KartikeyaMalimath/Frame-Interpolation-Using-AI-Model-for-Low-Bitrate-Video-Enhancement/assets/37095980/12aa48e6-b16d-44e3-863a-2d6f962c3808


### Reference Video


https://github.com/KartikeyaMalimath/Frame-Interpolation-Using-AI-Model-for-Low-Bitrate-Video-Enhancement/assets/37095980/fe82390f-cdb2-488e-ba01-8f5bfc67104b


### Stop Motion input Frames

![Stop-motion-frames-input](https://github.com/KartikeyaMalimath/Frame-Interpolation-Using-AI-Model-for-Low-Bitrate-Video-Enhancement/assets/37095980/cd2f8ce3-0c0e-44a7-be8e-ec4215a91904)

### Animated video from Stop motion Frames

https://github.com/KartikeyaMalimath/Frame-Interpolation-Using-AI-Model-for-Low-Bitrate-Video-Enhancement/assets/37095980/eabc5a4f-1745-4d88-b783-f8a3b422d7f4

## Future Work

1. Enhanced Model Integration
Objective: Improve low bitrate video quality through frame interpolation.
Current Approach: Utilizing the FILM model for sophisticated frame interpolation.
Consideration: Exploring the creation of a custom model for tailored optimization.
Prospective Benefits: Innovation, customization, and potential overcoming of limitations.
Challenges: Resource-intensive; careful evaluation of feasibility, benefits, and challenges.

2. Cloud Deployment and Scalability
Objective: Amplify scalability and accessibility of the frame interpolation application.
Approach: Investigating deployment on cloud platforms for high availability, scalability, and cost-efficiency.
Cloud Services: Video Intelligence API, Cloud Storage, Cloud CDN, and Cloud Transcoder API.
Expected Outcomes: Optimized performance, global accessibility, resource efficiency, and enhanced user experience.

3. User-Customized Interpolation
Objective: Enhance user engagement through customization of interpolation parameters.
Parameters: Motion magnitude and style for personalized video output.
Benefits: Greater user control, creative expression, and adaptation to individual preferences.
Implementation: Intuitive sliders, input fields, or preset options for accessible customization.
Consideration: Balancing complexity and usability to ensure a user-friendly interface.

4. Generating High FPS Videos from Stop Motion Images
Objective: Transform stop motion images into high frame rate videos.
Rationale: Enhance the aesthetics of classic stop motion animations.
Implementation Steps:
Input Sequence Preparation
Frame Interpolation
Output Video Generation
Applications: Enhanced aesthetics, modernization of classic content, enriched educational material, and artistic expression.
Challenges: Balancing authenticity, seamless integration, and optimizing processing.





