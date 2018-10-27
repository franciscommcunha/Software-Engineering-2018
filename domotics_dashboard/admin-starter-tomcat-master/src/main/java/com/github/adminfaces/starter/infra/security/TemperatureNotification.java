package com.github.adminfaces.starter.infra.security;

import org.omnifaces.util.Faces;
import javax.enterprise.inject.Specializes;
import javax.faces.context.FacesContext;
import javax.inject.Named;
import java.io.IOException;
import java.io.Serializable;
import static com.github.adminfaces.starter.util.Utils.addDetailMessage;
import javax.enterprise.context.SessionScoped;
import org.omnifaces.cdi.ViewScoped;

/**
 *
 * @author raquelramos
 */

@Named
@ViewScoped
public class TemperatureNotification implements Serializable {

    public static void temperatureHigh() throws IOException {
        addDetailMessage("Temperature is too <b>high</b>. Temperature will be decreased.");
        Faces.getExternalContext().getFlash().setKeepMessages(true);
        //Faces.redirect("index.xhtml");
    }
    
    public static void temperatureLow() throws IOException {
        addDetailMessage("Temperature is too <b>low</b>. Temperature will be increased.");
        Faces.getExternalContext().getFlash().setKeepMessages(true);
        //Faces.redirect("index.xhtml");
    }
}

