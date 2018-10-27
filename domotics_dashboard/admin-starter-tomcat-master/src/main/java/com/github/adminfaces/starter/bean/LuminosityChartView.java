/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.github.adminfaces.starter.bean;

/**
 *
 * @author raquelramos
 */
 
import javax.annotation.PostConstruct;
import java.io.Serializable;
import javax.faces.bean.ManagedBean;
import org.primefaces.model.chart.Axis;
import org.primefaces.model.chart.AxisType;
import org.primefaces.model.chart.BarChartModel;
import org.primefaces.model.chart.LineChartModel;
import org.primefaces.model.chart.ChartSeries;
import org.primefaces.model.chart.LineChartSeries;
 
@ManagedBean
public class LuminosityChartView implements Serializable {
 
    private LineChartModel lineModel1;

    @PostConstruct
    public void init() {
        createLineModels();
    }
 
    public LineChartModel getLineModel1() {
        return lineModel1;
    }
 
    private void createLineModels() {
        lineModel1 = initLinearModel();
        lineModel1.setTitle("Luminosity Chart");
        lineModel1.setLegendPosition("e");
        Axis xAxis = lineModel1.getAxis(AxisType.X);
        xAxis.setMin(0);
        xAxis.setMax(24);
        xAxis.setTickInterval("1");
        xAxis.setLabel("Hours");
        Axis yAxis = lineModel1.getAxis(AxisType.Y);
        yAxis.setMin(-0.5);
        yAxis.setMax(1.5);
        yAxis.setTickInterval("0.5");
        yAxis.setLabel("Luminosity");
    }
     
    private LineChartModel initLinearModel() {
        LineChartModel model = new LineChartModel();
 
        LineChartSeries series1 = new LineChartSeries();
        series1.setLabel("Kitchen");
 
        series1.set(0, 0);
        series1.set(4, 0);
        series1.set(12, 1);
        series1.set(17, 0);
        series1.set(20, 1);
        series1.set(22, 0);
 
        LineChartSeries series2 = new LineChartSeries();
        series2.setLabel("Living Room");
 
        series2.set(1, 0);
        series2.set(5, 0);
        series2.set(13, 0);
        series2.set(15, 0);
        series2.set(19, 1);
        series2.set(22, 1);
        series2.set(23, 1);
        
        LineChartSeries series3 = new LineChartSeries();
        series3.setLabel("Room 1");
 
        series3.set(3, 0);
        series3.set(8, 1);
        series3.set(11, 0);
        series3.set(14, 0);
        series3.set(16, 0);
        series3.set(22, 1);
        
        LineChartSeries series4 = new LineChartSeries();
        series4.setLabel("Room 2");
 
        series4.set(6, 17);
        series4.set(15, 14);
        series4.set(18, 15);
        series4.set(21, 21);
        series4.set(23, 24);
 
        model.addSeries(series1);
        model.addSeries(series2);
        model.addSeries(series3);
        model.addSeries(series4);
         
        return model;
    }
    
}