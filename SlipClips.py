  ffmpeg  -i Clip.mov -segment_start_number 1 -c copy -map 0 -segment_time 59 -reset_timestamps 1 -force_key_frames "expr:gte(t,n_forced*60)"  -f segment "SCP-009 The Zombie Virus %d.mov"
