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
import Vision

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
    
    lazy var classificationRequest: VNCoreMLRequest = {
        do {
            let model = try VNCoreMLModel(for: MNISTClassifier().model)
            return VNCoreMLRequest(
                model: model,
                completionHandler: self.handleClassification)
        } catch {
            fatalError("can't load Vision ML model: \(error)")
        }
    }()
    
    func handleClassification(request: VNRequest, error: Error?) {
        guard let observations = request.results as? [VNClassificationObservation]
            else { fatalError("unexpected result type from VNCoreMLRequest") }
        guard let best = observations.first else {
            fatalError("can't get best result")
        }
        print("\(observations)")
        DispatchQueue.main.async {
            self.textLabel.text = "Predicted: \(best.identifier) Confidence: \(best.confidence)"
        }
    }
    
    @IBAction func predict(_ sender: Any) {
        let image = preprocessImage()
        
        let handler = VNImageRequestHandler(ciImage: CIImage(image: image)!)
        do {
             try handler.perform([classificationRequest])
        } catch {
             print(error)
        }
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
}
