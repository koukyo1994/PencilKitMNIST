//
//  ViewController.swift
//  PencilKitMNIST
//
//  Created by 荒居秀尚 on 01.12.19.
//  Copyright © 2019 荒居秀尚. All rights reserved.
//

import UIKit
import PencilKit
import CoreML

class ViewController: UIViewController {
    
    var canvasView: PKCanvasView?
    
    @IBOutlet weak var imageView: UIImageView!
    @IBOutlet weak var textLabel: UILabel!
    
    static private let trainedImageSize = CGSize(width: 28, height: 28)
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let canvas = PKCanvasView(frame: imageView.frame)
        canvas.backgroundColor = .black

        view.addSubview(canvas)
        canvas.tool = PKInkingTool(.pen, color: .white, width: 20)
        
        self.canvasView = canvas
        
        if let window = UIApplication.shared.windows.first {
            if let toolPicker = PKToolPicker.shared(for: window) {
                toolPicker.addObserver(canvas)
                toolPicker.setVisible(true, forFirstResponder: canvas)
                canvas.becomeFirstResponder()
            }
        }
        
        textLabel.text = ""
    }
    
    // ML Detection
    func preprocessImage() -> UIImage {
        var image = canvasView!.drawing.image(
            from: canvasView!.drawing.bounds,
            scale: 10.0)
        
        if let newImage = UIImage(
            color: .black,
            size: CGSize(
                width: imageView.frame.width,
                height: imageView.frame.height
                )
            ) {
                if let overlayedImage = newImage.image(
                    byDrawingImage: image,
                    inRect: CGRect(
                        x: imageView.center.x,
                        y: imageView.center.y,
                        width: imageView.frame.width,
                        height: imageView.frame.width
                    )
                ) {
                    image = overlayedImage
            }
        }
        
        return image
    }
    
    func executePrediction(image: UIImage) {
        if let resizedImage = image.resize(newSize: Self.trainedImageSize), let pixelBuffer = resizedImage.toCVPixelBuffer() {
            guard let result = try? MNIST().prediction(image: pixelBuffer) else {
                print("error in image")
                return
            }
            
            self.textLabel.text = "Predicted: \(result.output)"
        }
    }
    
}
