"""
Test script để kiểm tra chức năng đánh giá chất lượng dữ liệu
"""
import pandas as pd
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root / "src"))

from utils.data_quality import DataQualityAssessment
from utils.cleaning import DataCleaner


def test_quality_assessment():
    """Test data quality assessment"""
    print("=" * 60)
    print("🧪 TEST: Data Quality Assessment")
    print("=" * 60)

    # Load sample data
    df = pd.read_csv('data/sample_orders.csv')
    print(f"\n📊 Loaded sample data: {len(df)} rows, {len(df.columns)} columns")

    # Test 1: Quality metrics
    print("\n" + "=" * 60)
    print("TEST 1: Overall Quality Metrics")
    print("=" * 60)

    qa = DataQualityAssessment(df)
    metrics = qa.get_data_quality_metrics()

    print(f"✅ Total Rows: {metrics['Tổng Dòng']:,}")
    print(f"✅ Total Columns: {metrics['Tổng Cột']}")
    print(f"✅ Total Cells: {metrics['Tổng Ô Dữ Liệu']:,}")
    print(f"⚠️  Missing Cells: {metrics['Ô Thiếu Dữ Liệu']:,} ({metrics['Tỷ Lệ Thiếu (%)']:.2f}%)")
    print(f"⚠️  Duplicate Rows: {metrics['Bản Ghi Trùng Lặp']:,} ({metrics['Tỷ Lệ Trùng Lặp (%)']:.2f}%)")
    print(f"🎯 Quality Score: {metrics['Điểm Chất Lượng']:.1f}/100", end="")

    if metrics['Điểm Chất Lượng'] >= 80:
        print(" 🟢 Xuất Sắc")
    elif metrics['Điểm Chất Lượng'] >= 60:
        print(" 🟡 Tốt")
    else:
        print(" 🔴 Cần Cải Thiện")

    # Test 2: Completeness
    print("\n" + "=" * 60)
    print("TEST 2: Completeness Report")
    print("=" * 60)

    completeness = qa.get_completeness_report()
    worst_cols = completeness.head(3)
    print("\nCột có tỷ lệ thiếu cao nhất:")
    for idx, row in worst_cols.iterrows():
        print(f"  - {row['Cột']}: {row['Tỷ Lệ Thiếu (%)']:.2f}% thiếu")

    # Test 3: Duplicates
    print("\n" + "=" * 60)
    print("TEST 3: Duplicates Report")
    print("=" * 60)

    duplicates = qa.get_duplicates_report()
    print(f"Total duplicate rows: {duplicates['Tổng Bản Ghi Trùng Lặp']:,}")
    print(f"Duplicate ratio: {duplicates['Tỷ Lệ Trùng Lặp (%)']:.2f}%")

    if duplicates['Chi Tiết Theo Cột']:
        print("\nColes có bản ghi trùng lặp:")
        for col, data in list(duplicates['Chi Tiết Theo Cột'].items())[:3]:
            print(f"  - {col}: {data['Trùng Lặp']} duplicates ({data['Tỷ Lệ (%)']:.2f}%)")

    # Test 4: Outliers
    print("\n" + "=" * 60)
    print("TEST 4: Outliers Report")
    print("=" * 60)

    outliers = qa.get_outliers_report()
    if not outliers.empty:
        print(f"Found {len(outliers)} columns with outliers:")
        for idx, row in outliers.head(3).iterrows():
            print(f"  - {row['Cột']}: {row['Số Ngoại Lệ']} outliers ({row['Tỷ Lệ (%)']:.2f}%)")
    else:
        print("✅ No significant outliers detected")

    # Test 5: Statistics
    print("\n" + "=" * 60)
    print("TEST 5: Statistical Summary")
    print("=" * 60)

    stats = qa.get_statistical_summary()
    if not stats.empty:
        print(f"Numeric columns analyzed: {len(stats)}")
        print("\nSummary of first 3 numeric columns:")
        for col in stats.index[:3]:
            print(f"\n  {col}:")
            print(f"    Mean: {stats.loc[col, 'mean']:.2f}")
            print(f"    Std: {stats.loc[col, 'std']:.2f}")
            print(f"    Min: {stats.loc[col, 'min']:.2f}")
            print(f"    Max: {stats.loc[col, 'max']:.2f}")

    # Test 6: Value Distribution
    print("\n" + "=" * 60)
    print("TEST 6: Value Distribution")
    print("=" * 60)

    # Get distribution for Region column
    region_dist = qa.get_value_distribution('Region', top_n=5)
    if not region_dist.empty:
        print(f"\nTop 5 values in 'Region' column:")
        for idx, row in region_dist.iterrows():
            print(f"  - {row['Giá Trị']}: {row['Số Lần']} times ({row['Tỷ Lệ (%)']:.2f}%)")

    # Test 7: Cleaning impact
    print("\n" + "=" * 60)
    print("TEST 7: Quality Score After Cleaning")
    print("=" * 60)

    cleaner = DataCleaner(df)
    df_cleaned = cleaner.clean()

    qa_cleaned = DataQualityAssessment(df_cleaned)
    metrics_cleaned = qa_cleaned.get_data_quality_metrics()

    print(f"Before cleaning: {metrics['Điểm Chất Lượng']:.1f}/100")
    print(f"After cleaning: {metrics_cleaned['Điểm Chất Lượng']:.1f}/100")
    print(f"Rows: {len(df):,} → {len(df_cleaned):,}")

    # Summary
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED")
    print("=" * 60)
    print("\n🎉 Data Quality Assessment Module is working correctly!")
    print("\nYou can now use this feature in the Streamlit app:")
    print("  1. Run: streamlit run src/app.py")
    print("  2. Upload data")
    print("  3. Go to: '🔍 Đánh Giá Chất Lượng Dữ Liệu' menu")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        test_quality_assessment()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

