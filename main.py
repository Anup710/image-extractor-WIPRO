# main.py - LLaVA-NeXT Mechanical Drawing Analyzer for columbus_drw/
import torch
import requests
from PIL import Image
from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration
import json
import re
import os
from pathlib import Path
import time
from typing import List, Dict, Any
import argparse
import io

class ColumbusDrawingAnalyzer:
    def __init__(self, model_name="llava-hf/llava-v1.6-mistral-7b-hf"):
        """Initialize the analyzer with LLaVA-NeXT model"""
        print(f"🔧 Columbus Drawing Analyzer - Loading {model_name}")
        print("⏳ Model loading (3-5 minutes on first run)...")
        
        # Load model and processor
        self.processor = LlavaNextProcessor.from_pretrained(model_name)
        self.model = LlavaNextForConditionalGeneration.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            device_map="auto",
            cache_dir="/workspace/columbus_drw/models"  # Cache in our directory
        )
        
        print(f"✅ Model loaded on device: {self.model.device}")
        
        # Mechanical drawing dimension patterns
        self.dimension_patterns = {
            'tolerance_dim': r'(\d+\.?\d*)\s*[±]\s*(\d+\.?\d*)',
            'diameter_symbol': r'[Ø∅]\s*(\d+\.?\d*)',
            'radius': r'R\s*(\d+\.?\d*)',
            'thread_spec': r'(\d+(?:\s*/\s*\d+)?)\s*[-‑]\s*(\d+)\s*(UNC|UNF|UNEF)\s*[-‑]\s*(\dA|\dB)',
            'chamfer': r'(\d+\.?\d*)\s*[Xx×]\s*(\d+\.?\d*)°?\s*[Cc]hamfer',
            'decimal_dim': r'\b(\d+\.\d{2,3})\b',
            'fractional_dim': r'(\d+)\s*(\d+/\d+)',
            'inspection_feature': r'\*\s*(\d+\.?\d*)\s*[±]?\s*(\d+\.?\d*)?'
        }

    def analyze_columbus_drawing(self, image_path: str, custom_prompt: str = None) -> Dict[str, Any]:
        """Analyze mechanical drawing optimized for Columbus hydraulics components"""
        
        # Load and prepare image
        try:
            if image_path.lower().endswith('.pdf'):
                # Convert PDF to image if needed
                print(f"📄 Converting PDF: {image_path}")
                image = self._convert_pdf_to_image(image_path)
            else:
                image = Image.open(image_path).convert('RGB')
        except Exception as e:
            raise Exception(f"Could not load image {image_path}: {e}")
        
        # Columbus-specific prompt for hydraulic components
        if custom_prompt is None:
            prompt = """<|im_start|>system
You are an expert mechanical engineer specializing in hydraulic systems and precision machining. You're analyzing technical drawings for Columbus Hydraulics components.

<|im_start|>user
<image>
Analyze this Columbus hydraulics mechanical drawing and extract ALL dimensions with their tolerances and geometric significance. This appears to be a piston assembly or hydraulic component.

For each dimension you identify:

1. **Exact Value & Tolerance**: Extract the precise numerical value and tolerance (e.g., "2.490 ±0.002")

2. **Geometric Significance**: Identify what each dimension controls:
   - Piston diameters (main, lands, grooves)
   - Shaft diameters and lengths
   - Seal groove dimensions (width, depth)
   - Threading specifications (UNF, UNC)
   - Chamfers and radii
   - Critical inspection dimensions (marked with *)
   - Hydraulic port dimensions

3. **Functional Purpose**: Explain the hydraulic/mechanical function:
   - Sealing surfaces
   - Bearing surfaces
   - Pressure containment
   - Assembly interfaces

4. **Manufacturing Notes**: Note any:
   - Surface finish requirements
   - Tool chatter restrictions
   - Material specifications
   - Heat treatment callouts

Pay special attention to:
- Columbus part numbering system
- Inspection/sampling features (*)
- Thread specifications for hydraulic fittings
- Seal groove critical dimensions
- Piston-to-cylinder clearances

Format your response with clear sections for dimensions, threads, inspection features, and manufacturing notes.

<|im_start|>assistant"""
        else:
            prompt = custom_prompt

        # Process inputs
        inputs = self.processor(prompt, image, return_tensors="pt").to(self.model.device)
        
        print("🔍 Running LLaVA-NeXT inference...")
        start_time = time.time()
        
        # Generate response
        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_new_tokens=1500,  # Longer for detailed analysis
                do_sample=False,
                temperature=0.1,
                pad_token_id=self.processor.tokenizer.eos_token_id
            )
        
        # Decode response
        response = self.processor.decode(output[0], skip_special_tokens=True)
        
        # Extract only the assistant's response
        if "<|im_start|>assistant" in response:
            response = response.split("<|im_start|>assistant")[-1].strip()
        
        inference_time = time.time() - start_time
        print(f"✅ Analysis completed in {inference_time:.2f} seconds")
        
        return {
            'llava_response': response,
            'image_path': image_path,
            'inference_time': inference_time,
            'model_device': str(self.model.device),
            'image_size': image.size
        }

    def _convert_pdf_to_image(self, pdf_path: str) -> Image:
        """Convert PDF to image for analysis"""
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(pdf_path)
            page = doc[0]  # First page
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x scale for better quality
            img_data = pix.tobytes("ppm")
            image = Image.open(io.BytesIO(img_data))
            doc.close()
            return image
        except ImportError:
            raise Exception("PyMuPDF not installed. Install with: pip install PyMuPDF")

    def extract_dimensions_regex(self, text: str) -> List[Dict]:
        """Extract dimensions using regex patterns optimized for Columbus drawings"""
        dimensions = []
        text_lines = text.split('\n')
        
        for line_num, line in enumerate(text_lines):
            for pattern_name, pattern in self.dimension_patterns.items():
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    dim_info = {
                        'type': pattern_name,
                        'value': match.group(1) if match.groups() else match.group(0),
                        'tolerance': match.group(2) if len(match.groups()) > 1 else None,
                        'full_match': match.group(0),
                        'line_number': line_num + 1,
                        'line_text': line.strip(),
                        'confidence': self._calculate_confidence(pattern_name, match.group(0))
                    }
                    dimensions.append(dim_info)
        
        return dimensions

    def _calculate_confidence(self, pattern_type: str, match_text: str) -> float:
        """Calculate confidence score for extracted dimensions"""
        base_confidence = {
            'tolerance_dim': 0.9,
            'diameter_symbol': 0.95,
            'thread_spec': 0.98,
            'inspection_feature': 0.95,
            'chamfer': 0.85,
            'radius': 0.85,
            'decimal_dim': 0.7,
            'fractional_dim': 0.6
        }
        
        conf = base_confidence.get(pattern_type, 0.5)
        
        # Boost confidence for typical hydraulic dimensions
        if any(keyword in match_text.lower() for keyword in ['2.49', '2.47', '1.00', '0.81']):
            conf += 0.1
            
        return min(conf, 1.0)

    def comprehensive_analysis(self, image_path: str) -> Dict[str, Any]:
        """Complete Columbus drawing analysis"""
        print(f"\n{'='*80}")
        print(f"🔧 COLUMBUS HYDRAULICS DRAWING ANALYSIS")
        print(f"📁 File: {os.path.basename(image_path)}")
        print(f"{'='*80}")
        
        # Primary LLaVA-NeXT analysis
        llava_result = self.analyze_columbus_drawing(image_path)
        
        # Regex backup extraction
        regex_dimensions = self.extract_dimensions_regex(llava_result['llava_response'])
        
        # Analyze drawing metadata
        drawing_metadata = self._extract_drawing_metadata(llava_result['llava_response'])
        
        # Compile complete analysis
        analysis = {
            'drawing_file': os.path.basename(image_path),
            'full_path': image_path,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'analysis_results': {
                'llava_detailed_response': llava_result['llava_response'],
                'extracted_dimensions': regex_dimensions,
                'drawing_metadata': drawing_metadata,
                'performance_metrics': {
                    'inference_time_seconds': llava_result['inference_time'],
                    'model_device': llava_result['model_device'],
                    'image_dimensions': llava_result['image_size'],
                    'total_dimensions_found': len(regex_dimensions),
                    'high_confidence_dims': len([d for d in regex_dimensions if d['confidence'] > 0.8])
                }
            }
        }
        
        return analysis

    def _extract_drawing_metadata(self, response: str) -> Dict:
        """Extract drawing metadata like part number, material, etc."""
        metadata = {}
        
        # Look for common drawing info
        patterns = {
            'part_number': r'(?:part|drawing|no\.?|number)\s*:?\s*([A-Z0-9\-\.]+)',
            'material': r'(?:material|mat\'l)\s*:?\s*([A-Z0-9\s\-]+)',
            'scale': r'(?:scale)\s*:?\s*([\d\.:]+)',
            'weight': r'(?:weight)\s*:?\s*([\d\.]+\s*\w+)',
            'revision': r'(?:rev|revision)\s*:?\s*([A-Z0-9]+)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                metadata[key] = match.group(1).strip()
        
        return metadata

def setup_columbus_workspace():
    """Setup workspace for Columbus drawings analysis"""
    base_dir = Path("/workspace/columbus_drw")
    
    # Create directory structure
    dirs = ['images', 'results', 'logs', 'models', 'processed']
    for dir_name in dirs:
        (base_dir / dir_name).mkdir(parents=True, exist_ok=True)
        print(f"📁 Directory ready: {dir_name}/")
    
    return base_dir

def main():
    parser = argparse.ArgumentParser(description='Columbus Hydraulics Drawing Analyzer')
    parser.add_argument('--image', type=str, help='Single image file path')
    parser.add_argument('--batch', action='store_true', help='Process all images in images/')
    parser.add_argument('--model', type=str, default='llava-hf/llava-v1.6-mistral-7b-hf')
    parser.add_argument('--output-dir', type=str, default='results', help='Output directory')
    
    args = parser.parse_args()
    
    print("🚀 COLUMBUS HYDRAULICS DRAWING ANALYZER")
    print("=" * 60)
    
    # Setup workspace
    base_dir = setup_columbus_workspace()
    os.chdir(base_dir)
    
    # Initialize analyzer
    print("\n🔧 Initializing LLaVA-NeXT for Columbus drawings...")
    analyzer = ColumbusDrawingAnalyzer(model_name=args.model)
    
    results_dir = Path(args.output_dir)
    results_dir.mkdir(exist_ok=True)
    
    if args.batch:
        print(f"\n📁 Batch processing mode - scanning images/ directory...")
        
        # Find all image files
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.pdf', '*.tiff', '*.bmp']
        image_files = []
        for ext in image_extensions:
            image_files.extend(Path('images').glob(ext))
            image_files.extend(Path('images').glob(ext.upper()))
        
        if not image_files:
            print("❌ No images found in images/ directory")
            print("   Supported formats: JPG, PNG, PDF, TIFF, BMP")
            return
        
        print(f"📷 Found {len(image_files)} images to process")
        
        # Process each image
        for i, image_file in enumerate(image_files, 1):
            print(f"\n📊 Processing {i}/{len(image_files)}: {image_file.name}")
            try:
                analysis = analyzer.comprehensive_analysis(str(image_file))
                
                # Save results
                output_file = results_dir / f"{image_file.stem}_columbus_analysis.json"
                with open(output_file, 'w') as f:
                    json.dump(analysis, f, indent=2, default=str)
                
                # Print summary
                metrics = analysis['analysis_results']['performance_metrics']
                print(f"   ✅ Complete - {metrics['total_dimensions_found']} dimensions found")
                print(f"   ⏱️  Processing time: {metrics['inference_time_seconds']:.1f}s")
                print(f"   💾 Saved to: {output_file.name}")
                
                # Move processed image
                processed_dir = Path('processed')
                processed_file = processed_dir / image_file.name
                try:
                    image_file.rename(processed_file)
                    print(f"   📁 Moved to: processed/{image_file.name}")
                except:
                    pass  # Keep original if move fails
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
    
    elif args.image:
        print(f"\n🖼️ Single image analysis: {args.image}")
        
        if not os.path.exists(args.image):
            print(f"❌ Image not found: {args.image}")
            return
        
        try:
            analysis = analyzer.comprehensive_analysis(args.image)
            
            # Save results
            output_file = results_dir / f"{Path(args.image).stem}_columbus_analysis.json"
            with open(output_file, 'w') as f:
                json.dump(analysis, f, indent=2, default=str)
            
            # Display detailed results
            print(f"\n📋 DETAILED COLUMBUS ANALYSIS RESULTS")
            print("=" * 60)
            
            llava_response = analysis['analysis_results']['llava_detailed_response']
            print("🔍 LLaVA-NeXT Analysis:")
            print("-" * 40)
            print(llava_response[:1000] + "..." if len(llava_response) > 1000 else llava_response)
            
            dims = analysis['analysis_results']['extracted_dimensions']
            print(f"\n📏 Extracted Dimensions ({len(dims)} found):")
            print("-" * 40)
            for dim in dims[:10]:  # Show first 10
                print(f"  {dim['type']}: {dim['full_match']} (confidence: {dim['confidence']:.2f})")
            
            metadata = analysis['analysis_results']['drawing_metadata']
            if metadata:
                print(f"\n📄 Drawing Metadata:")
                print("-" * 40)
                for key, value in metadata.items():
                    print(f"  {key}: {value}")
            
            print(f"\n💾 Results saved to: {output_file}")
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
    
    else:
        print("\n⚠️ No input specified!")
        print("Usage:")
        print("  python main.py --image images/your_drawing.pdf")
        print("  python main.py --batch")
        print("\n📁 Upload your Columbus drawings to: images/")

if __name__ == "__main__":
    main()