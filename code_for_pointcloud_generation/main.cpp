#include <iostream>
#include <vector>
#include <string>
#include <boost/function.hpp>
#include <pcl/io/pcd_io.h>
#include <pcl/io/ply_io.h>
#include <pcl/io/image_grabber.h>
#include <pcl/visualization/cloud_viewer.h>
#include <pcl/filters/approximate_voxel_grid.h>
#include <pcl/registration/icp.h>

#define HEADLESS

pcl::ImageGrabber<pcl::PointXYZRGB> *interface;
#ifndef HEADLESS
pcl::visualization::PCLVisualizer::Ptr viewer_merged(new pcl::visualization::PCLVisualizer("merged"));
#endif
//pcl::visualization::CloudViewer viewer_single("single");
pcl::ApproximateVoxelGrid<pcl::PointXYZRGB> filter;
pcl::IterativeClosestPoint<pcl::PointXYZRGB, pcl::PointXYZRGB> icp;
pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud_merged(new pcl::PointCloud<pcl::PointXYZRGB>);
pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud_single(new pcl::PointCloud<pcl::PointXYZRGB>);
std::string workdir;

void cloud_cb(const pcl::PointCloud<pcl::PointXYZRGB>::ConstPtr &cloud)
{
    static int iter = 0;
    std::cout << interface->getCurrentDepthFileName() << std::endl;
    pcl::copyPointCloud(*cloud, *cloud_single);
    std::vector<int> indices;
    pcl::removeNaNFromPointCloud(*cloud_single, *cloud_single, indices);
    std::cout << "Original Size: " << cloud_single->size() << std::endl;
    filter.setInputCloud(cloud_single);
    filter.filter(*cloud_single);
    std::cout << "Filtered Size: " << cloud_single->size() << std::endl;
    iter++;
    pcl::io::savePLYFileBinary(workdir + "/orig_" + std::to_string(iter) + ".ply", *cloud_single);
    if(cloud_merged->size() == 0) {
        pcl::copyPointCloud(*cloud_single, *cloud_merged);
#ifndef HEADLESS
        viewer_merged->setBackgroundColor(0, 0, 0);
        viewer_merged->addPointCloud(cloud_merged, "cloud");
        viewer_merged->setPointCloudRenderingProperties(pcl::visualization::PCL_VISUALIZER_POINT_SIZE, 5, "cloud");
        viewer_merged->addCoordinateSystem(1.0);
        viewer_merged->initCameraParameters();
#endif
        return;
    }
    icp.setInputSource(cloud_merged);
    icp.setInputTarget(cloud_single);
    // Set the max correspondence distance to 5cm (e.g., correspondences with higher distances will be ignored)
    icp.setMaxCorrespondenceDistance(0.1);
    // Set the maximum number of iterations (criterion 1)
    icp.setMaximumIterations(200);
    // Set the transformation epsilon (criterion 2)
    //icp.setTransformationEpsilon (1e-8);
    // Set the euclidean distance difference epsilon (criterion 3)
    //icp.setEuclideanFitnessEpsilon (1);
    icp.align(*cloud_merged);
    //if((++iter) % 3) return;
    *cloud_merged += *cloud_single;
    filter.setInputCloud(cloud_merged);
    filter.filter(*cloud_merged);
    std::cout << "Merged Size: " << cloud_merged->size() << std::endl << std::endl;
#ifndef HEADLESS
    viewer_merged->updatePointCloud(cloud_merged, "cloud");
#endif
    //if((++iter) % 10) return;
    pcl::io::savePLYFileBinary(workdir + "/" + std::to_string(iter) + ".ply", *cloud_merged);
}

int main(int argc, char *argv[])
{
    workdir = argv[1];
    std::cout << "workdir: " << workdir << std::endl;
    filter.setLeafSize(0.01, 0.01, 0.01);
    interface = new pcl::ImageGrabber<pcl::PointXYZRGB>(workdir, 1);
    interface->setCameraIntrinsics(294, 294, 160, 120);
    boost::function<void (const pcl::PointCloud<pcl::PointXYZRGB>::ConstPtr &)> f = cloud_cb;
    interface->registerCallback(f);
    interface->start();
    //boost::this_thread::sleep(boost::posix_time::seconds(10));
    while(interface->isRunning())
    {
#ifndef HEADLESS
        viewer_merged->spinOnce(1000);
#else
        boost::this_thread::sleep(boost::posix_time::seconds(1));
#endif
    }
    return 0;
}
