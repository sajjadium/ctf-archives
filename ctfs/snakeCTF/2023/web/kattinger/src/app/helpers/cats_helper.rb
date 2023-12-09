module CatsHelper
    require 'curl'
    require 'rmagick'
    require 'base64'
    require 'timeout'

    include Magick

    def process_image(image_path)        
        p "Processing: " + image_path
        image_path = image_path.encode!("utf-8").scrub()
        if image_path.start_with?('http') || image_path.start_with?('https')
            curl = CURL.new({:cookies_disable => false})
            curl.debug=true
            p image_path
            filename = Timeout::timeout(3) do
                curl.save!(image_path)
            end
            p filename
        else
            filename = image_path
        end
        processed = ImageList.new(image_path)
        processed = processed.solarize(100)
        result = 'data://image;base64,' + Base64.strict_encode64(processed.to_blob())
        File.unlink(filename)
        return result

    end
end
